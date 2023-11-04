from django.urls import path,include
from .views import *
from .views import *

urlpatterns = [
    path('register/',Register, name='register'),
    path('login/',Login, name='login'),
    path('logout/',Logout, name='logout'),
    
]