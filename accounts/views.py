from django.shortcuts import render,redirect
from.forms import *
from django.contrib.auth import login

# Create your views here.
def Register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks') 
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})