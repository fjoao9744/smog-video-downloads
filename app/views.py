from django.shortcuts import render
from django.http import FileResponse, HttpResponse, JsonResponse
from celery.result import AsyncResult
from celery import current_app
from .tasks import dowload_videos
import os

def index(request):
    if request.method == "POST":
        url = request.POST.get("url")
        
        task = dowload_videos.delay(url)
        
        
        return render(request, "index.html", {"task_id": task.id})
    
    return render(request, "index.html")
        
def download(request, video_id):
    for file in os.listdir('static/media/videos'):
        if file.startswith(video_id):
            filepath = os.path.join('static/media/videos', file)
            f = open(filepath, 'rb') 
            return FileResponse(f, as_attachment=True, filename=file)
    return HttpResponse("File not found.", status=404)

def task_status(request, task_id):
    task = AsyncResult(task_id, app=current_app)

    if task.state == 'SUCCESS':
        result = task.result
        if result is None:
            return JsonResponse({"status": "error", "message": "Erro: Unable to download video."}, status=500)

        return JsonResponse({
            "status": "finished",
            "video_id": result.get("id"),
            "title": result.get("title"),
        })

    elif task.state == 'FAILURE':
        return JsonResponse({
            "status": "error",
            "message": str(task.result),  # mostra o erro da exceção
        }, status=500)

    else:
        return JsonResponse({"status": task.state})
