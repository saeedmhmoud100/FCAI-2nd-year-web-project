from django.contrib.auth import login, authenticate, get_user_model
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import  messages

from accounts.forms import SignUpForm

# Create your views here.

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})

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
                messages.add_message(request,messages.ERROR, 'Passwords do not match')
            elif User.objects.filter(Q(username=username)):
                messages.add_message(request,messages.ERROR, 'Username already exists')
            elif User.objects.filter(Q(email=email)):
                messages.add_message(request,messages.ERROR, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                if is_admin:
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                login(request, user)
                return redirect('profile')

    else:
        form = SignUpForm()

    return render(request, 'accounts/sign_up.html', {'form': form})