from django.shortcuts import render,redirect
from.forms import *
from django.contrib.auth import login, authenticate, logout
import logging
from django.contrib import messages

logger = logging.getLogger(__name__)

# Create your views here.
def Register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            # Check if username already exists
            if CustomUser.objects.filter(username=username).exists():
                form.add_error('username', forms.ValidationError('Username already exists'))
                return render(request, 'register.html', {'form': form})

            # Check if email already exists
            if CustomUser.objects.filter(email=email).exists():
                form.add_error('email', forms.ValidationError('Email already exists'))
                return render(request, 'register.html', {'form': form})

            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def Login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials')  # Add error message here
                logger.error('Invalid login credentials')
                return redirect('login')

    return render(request, 'login.html', {'form': form})


def Logout(request):
    logout(request)  
    return redirect('login')