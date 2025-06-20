from django.shortcuts import render
from yt_dlp import YoutubeDL
from django.http import FileResponse, HttpResponse
import os

def index(request):
    if request.method == "POST":
        url = request.POST.get("url")
        
        ydl_opts = {
            'cookiefile': "cookies.txt",
            'writethumbnail': True,
            'format': 'best',
            'outtmpl': 'static/media/videos/%(id)s.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            if info is None:
                return HttpResponse("Erro: Unable to download video.", status=500)
            
            video_id = info.get('id')
        
        return render(request, "index.html", {"info":info.get("title"), "video_id":video_id, "thumb": f"static/media/videos/{video_id}.webp"})
    
    return render(request, "index.html")
        
def download(request, video_id):
    for file in os.listdir('static/media/videos'):
        if file.startswith(video_id):
            filepath = os.path.join('static/media/videos', file)
            f = open(filepath, 'rb') 
            return FileResponse(f, as_attachment=True, filename=file)
    return HttpResponse("File not found.", status=404)
    