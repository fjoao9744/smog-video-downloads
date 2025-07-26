from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("download/<str:video_id>", views.download, name="download"),
    path("task-status/<str:task_id>", views.task_status, name='task_status')
]
