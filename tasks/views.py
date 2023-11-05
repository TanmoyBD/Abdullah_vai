from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import *
from .serializers import *
from.forms import *

def Home(request):
    return render(request, 'home.html')

def Create_Task(request):
    return render(request, 'create_task.html')

def Completed_Task(request):
    return render(request,'completed_task.html')

def Task_Details(request,task_id):
    return render(request,'task_details.html')



def Edit_Task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'edit_task.html', {'form': form, 'task': task})


#JSON FORMAT_____________________________________________
# def get_user_tasks(request, user_id):
#     tasks = Task.objects.filter(user_id=user_id)
#     serializer = TaskSerializer(tasks, many=True)
#     return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_user_tasks(request):
    if request.method == 'GET':
        user = request.user
        tasks = Task.objects.filter(user=user, completed=False).order_by('-priority_choice')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully.'})

    
    
@api_view(['POST'])
def create_task_api(request):
    print("Dhukce")
    if request.method == 'POST':
        print(request.data)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data) 
            serializer.save(user=request.user)
            return JsonResponse({'message': 'Task created successfully.'})
        else:
            print(serializer.errors)
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)
    
    
    
    
def get_completed_tasks(request):
    user = request.user
    completed_tasks = Task.objects.filter(user=user, completed=True)
    
    task_list = []
    for task in completed_tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority_choice': task.get_priority_choice_display(),
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'completed': task.completed,
            'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': task.updated_at.strftime('%Y-%m-%d %H:%M:%S') if task.updated_at else None,
        }
        task_list.append(task_data)
    
    return JsonResponse(task_list, safe=False)

class TaskDetailsView(View):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'priority_choice': task.priority_choice,
                'completed': task.completed,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat()
            }
            return JsonResponse(data)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)