from django import forms  
from .models import Task

class TaskForm(forms.ModelForm): # 👈 tells Django to auto-generate form fields
    class Meta:
        model = Task
        fields = ["title", "complete"]