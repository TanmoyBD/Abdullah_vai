from django.urls import path,include
from .views import *


urlpatterns = [
    path('',Home, name='home'),
    path('create/task/',Create_Task, name='add_task'),
    
    
    path('api/user_tasks/', get_user_tasks, name='get_user_tasks'),
    path('api/delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('api/create_task/', create_task_api, name='create_task'),
    
]