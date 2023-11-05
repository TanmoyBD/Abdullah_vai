from django.urls import path,include
from .views import *


urlpatterns = [
    path('',Home, name='home'),
    path('create/task/',Create_Task, name='add_task'),
    path('edit_task/<int:task_id>/', Edit_Task, name='edit_task'),
    path('completed/tasks/', Completed_Task, name='completed_task'),
    path('details/<int:task_id>/', Task_Details, name='task_details'),
    
    
    path('api/user_tasks/', get_user_tasks, name='get_user_tasks'),
    path('api/delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('api/create_task/', create_task_api, name='create_task'),
    path('api/completed_tasks/', get_completed_tasks, name='completed_tasks_api'),
    path('api/task_details/<int:task_id>/', TaskDetailsView.as_view(), name='task_details_api'),
    
]