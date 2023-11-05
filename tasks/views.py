from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import *
from .serializers import *

def Home(request):
    return render(request, 'home.html')


def Create_Task(request):
    return render(request, 'create_task.html')


#JSON FORMAT_____________________________________________
# def get_user_tasks(request, user_id):
#     tasks = Task.objects.filter(user_id=user_id)
#     serializer = TaskSerializer(tasks, many=True)
#     return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_user_tasks(request):
    if request.method == 'GET':
        user = request.user  # Assuming you're using authentication
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
            print(serializer.errors)  # Print any validation errors
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)
    
    
