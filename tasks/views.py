from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm


# Create your views here.
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks":tasks})

def create_task(request):
    if request.method == "POST": # if user used submit
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = TaskForm()  
    return render(request, "tasks/create_task.html",{"form": form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else: 
        form = TaskForm(instance=task)
    return render(request, "tasks/edit_task.html", {"form":form})       

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    
    return render(request, "tasks/delete_task.html", {"task":task})

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.complete = not task.complete # flip
    task.save()
    # If it's an AJAX call (from JS)
     # Return JSON so JS can update the icon
    return JsonResponse({"complete": task.complete})


