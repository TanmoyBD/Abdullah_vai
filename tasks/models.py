
from django.db import models
from accounts.models import CustomUser

class Task(models.Model):
    
    P_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        
    )

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority_choice = models.IntegerField(choices=P_CHOICES, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


