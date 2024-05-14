from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from accounts.forms import SignUpForm, UserForm, UserUpdateForm
from project.permissions import is_not_authenticated, check_authenticated, check_user, is_admin

# Create your views here.

User = get_user_model()
not_auth_required = user_passes_test(is_not_authenticated, login_url='profile')
is_admin_required = user_passes_test(is_admin, login_url='profile')

@not_auth_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username or password')
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


@not_auth_required
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            re_password = form.cleaned_data.get('re_password')
            is_admin = form.cleaned_data.get('is_admin')
            print(username, email, password, re_password, is_admin)
            if password != re_password:
                messages.add_message(request, messages.ERROR, 'Passwords do not match')
            elif User.objects.filter(Q(username=username)):
                messages.add_message(request, messages.ERROR, 'Username already exists')
            elif User.objects.filter(Q(email=email)):
                messages.add_message(request, messages.ERROR, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                if is_admin:
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                # login(request, user)
                messages.add_message(request, messages.SUCCESS, 'the account is registered successfully')
                return redirect('login')

    else:
        form = SignUpForm()

    return render(request, 'accounts/sign_up.html', {'form': form})


@check_authenticated(check_user)
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


@is_admin_required
@check_authenticated(check_user)
def change_active_status(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('dashboard_user_list')


@check_authenticated(check_user)
def delete_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.delete()
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('profile')
    return render(request, 'accounts/delete_user.html', {'object': User.objects.get(id=user_id)})


@is_admin_required
@check_authenticated(check_user)
def change_user_rule(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_staff and user.is_superuser:
        user.is_staff = False
        user.is_superuser = False
    else:
        user.is_staff = True
        user.is_superuser = True
    user.save()
    return redirect('dashboard_user_list')


class CreateUserView(UserPassesTestMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/add_user.html'

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        user = super().form_valid(form)
        if form.cleaned_data.get('is_admin'):
            self.object.is_staff = True
            self.object.is_superuser = True
            self.object.save()
        return user

    def get_success_url(self):
        return reverse('dashboard_user_list')


class UserProfileView(UserPassesTestMixin,View):
    def get(self, request):
        user = request.user
        return render(request, 'accounts/user_profile.html', {'user': user})

    def test_func(self):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR, 'You need to login to view this page')
        return self.request.user.is_authenticated

    def post(self, request):
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')
        if not current_password or not new_password or not re_password:
            messages.add_message(request, messages.ERROR, 'All fields are required')
        else:
            if user.check_password(current_password):
                if new_password == re_password:
                    user.set_password(new_password)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Password changed successfully')
                else:
                    messages.add_message(request, messages.ERROR, 'Passwords do not match')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid current password')

        return redirect('profile')


class UpdateUserView(UserPassesTestMixin,UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/update_user.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs.get('pk')
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Data updated successfully')
        return reverse('profile')

    def form_invalid(self, form):
        for field in form.errors:
            messages.add_message(self.request, messages.ERROR, f'{field}: {form.errors[field][0]}')
        return super().form_invalid(form)
