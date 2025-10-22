# 📝 Django To-Do App

A simple, modern To-Do List application built with **Django** and **vanilla JavaScript (AJAX)**.  
You can add, edit, delete, and toggle task completion — instantly, without page reloads.

---

## 🚀 Features

✅ Create new tasks  
✅ Edit existing tasks  
✅ Delete tasks  
✅ Toggle completion status (AJAX)  
✅ Persistent database (SQLite)  
✅ Responsive UI with static CSS + JS  

---

## 🏗️ Project Setup

### 1️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate    # Windows
# or
source venv/bin/activate # Mac/Linux

pip install django

django-admin startproject todo_project
cd todo_project

python manage.py startapp tasks

INSTALLED_APPS = [
    ...,
    'tasks',
]

tasks/models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

python manage.py makemigrations
python manage.py migrate

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'complete']

tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})

def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/create_task.html", {"form": form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/edit_task.html", {"form": form})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "tasks/delete_task.html", {"task": task})

def toggle_task(request, task_id):
    if request.method == "POST":
        try:
            task = Task.objects.get(id=task_id)
            task.complete = not task.complete
            task.save()
            return JsonResponse({"status": "success", "complete": task.complete})
        except Task.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Task not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
]

todo_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]

Folder Structure
tasks/
 ├── static/
 │   └── tasks/
 │       ├── css/style.css
 │       └── js/script.js
 └── templates/
     └── tasks/
         ├── base.html
         ├── task_list.html
         ├── create_task.html
         ├── edit_task.html
         └── delete_task.html

base.html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Todo App{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'tasks/css/style.css' %}">
  <script src="{% static 'tasks/js/script.js' %}" defer></script>
</head>
<body>
  <header>
    <h1><a href="/">My Todo List</a></h1>
    <nav>
      <a href="/">Home</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
    </nav>
    <hr>
  </header>

  <main>
    {% block content %}{% endblock %}
  </main>
</body>
</html>

script.js
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("li[data-id]").forEach(item => {
    item.addEventListener("click", async () => {
      const taskId = item.dataset.id;
      const response = await fetch(`/toggle/${taskId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          "X-Requested-With": "XMLHttpRequest"
        },
      });
      const data = await response.json();
      if (data.status === "success") {
        item.classList.toggle("completed", data.complete);
      }
    });
  });
});

function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

style.css
body {
  font-family: Arial, sans-serif;
  margin: 20px;
}

.completed {
  text-decoration: line-through;
  color: gray;
}

a {
  margin: 0 5px;
}
