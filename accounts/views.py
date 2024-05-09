from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect

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
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password2 = request.POST.get('re-password')
        if password == re_password2:
            u = User.objects.create(username=username, email=email, password=password)
            if request.POST.get('is_admin') == 'true':
                u.is_admin = True
                u.is_staff = True
            u.save()
        else:
            return render(request, 'accounts/sign_up.html', {'error': 'Password does not match'})


    return render(request, 'accounts/sign_up.html')
