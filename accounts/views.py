from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


# Create your views here.

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