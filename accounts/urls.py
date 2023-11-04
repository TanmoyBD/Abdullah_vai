from django.urls import path,include
from .views import *
from .views import *

urlpatterns = [
    path('register/',Register, name='register'),
    #path('login/',CustomLoginView.as_view(), name='login'),
    #path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    
]