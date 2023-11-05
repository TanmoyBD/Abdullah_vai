from django.shortcuts import render,redirect
from.forms import *
from .models import *
from django.contrib.auth import login, authenticate, logout
import logging
from django.contrib import messages
import uuid
import random
from django.core.mail import EmailMessage

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





#Password rest syestem________________________________________________________________________


def generate_confirmation_code():
    confirmation_code = ''.join(random.choice('0123456789') for _ in range(6))
    return confirmation_code



def Send_mail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return render(request, 'email_submit.html', {'error_message': 'Email not found'})
    
        confirmation_code = generate_confirmation_code()
        
        user.confirmation_code=confirmation_code
        user.save()
        
        mail_subject = 'Forgot password'
        message = f'Hi {user.username} Your verification code is: {confirmation_code}'
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        return redirect('confirmation', email=email,username=user.username)
    return render(request, 'email_submit.html')



def Confirmation(request,email,username):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        print("Line 102 ")
        if form.is_valid():
            print("line to 193")
            user = CustomUser.objects.filter(email=email).first()
            original_code = user.confirmation_code
            user_given_code = form.cleaned_data['confirmation_code']
            
            print("The code is",original_code)
            
            if original_code == user_given_code:
                random_token = str(uuid.uuid4())
                print("line to 197")
                
                # Assign the token to user.forgotten_token
                user.forgotten_token = random_token
                user.save()
                user.confirmation_code = None
                return redirect('forgot_pass',pass_rest_token=random_token)
            else:
                form.add_error('confirmation_code','Enter the correct code.')
    else:
        form = ConfirmationForm()

    return render(request, 'confirmation.html', {'form': form,'username':username,'email':email})





def Forgotten_password(request, pass_rest_token):
    try:
        
        user = CustomUser.objects.get(forgotten_token=pass_rest_token)
        print("Here are token",pass_rest_token)
    except CustomUser.DoesNotExist:
        return render(request, 'login.html')

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password == confirm_password:
                user.set_password(new_password)
                user.forgotten_token = None
                user.confirmation_code = None
                user.save()
                return redirect('login')
            else:
                form.add_error('confirm_password', 'Passwords do not match.')
        else:
            form.add_error('confirm_password', 'Passwords do not match.')
    else:
        form = PasswordChangeForm()

    return render(request, 'password_change.html', {'form': form})
