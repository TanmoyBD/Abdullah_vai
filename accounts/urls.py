from django.urls import path,include
from .views import *
from .views import *

urlpatterns = [
    path('register/',Register, name='register'),
    path('login/',Login, name='login'),
    path('logout/',Logout, name='logout'),
    #Forgot password syestem__________________________________________________________________
    path('forgot_password/', Send_mail, name='send_mail'),
    path('confirmation/<str:email>/<str:username>/', Confirmation, name='confirmation'),
    path('pass_word_rest/<str:pass_rest_token>/', Forgotten_password, name='forgot_pass'),
    
]