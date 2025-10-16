from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name= "task_list" ),
    path("create", views.create_task, name="create_task"), #new add reroute
    path("edit/<str:task_id>", views.edit_task, name="edit_task"), #new update route
    path("delete/<str:task_id>",views.delete_task, name='delete_task'), # delete task
    path("toggle/<int:task_id>/", views.toggle_task, name="toggle_task"),
]