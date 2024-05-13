from django.contrib.auth import login, authenticate, get_user_model, logout
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import SignUpForm, UserForm

# Create your views here.

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username or password')
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


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


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


def change_active_status(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('dashboard_user_list')

def delete_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.delete()
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('dashboard_user_list')
    return render(request, 'accounts/delete_user.html')

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


class CreateUserView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/add_user.html'

    def form_valid(self, form):
        user= super().form_valid(form)
        if form.cleaned_data.get('is_admin'):
            self.object.is_staff = True
            self.object.is_superuser = True
            self.object.save()
        return user

    def get_success_url(self):
        return reverse('dashboard_user_list')

