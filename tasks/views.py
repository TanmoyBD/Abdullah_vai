from django.shortcuts import render

def Home(request):
    print("HOOOOOOMEEEE")
    return render(request, 'home.html')