from django.shortcuts import render
from yt_dlp import YoutubeDL
from django.http import FileResponse, HttpResponse
import os

def index(request):
    if request.method == "POST":
        url = request.POST.get("url")
        
        ydl_opts = {
            'cookiefile': "cookies.txt",
            'format': 'best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            if info is None:
                return HttpResponse("Erro: não foi possível baixar o vídeo.", status=500)
            
            video_id = info.get('id')
        
        return render(request, "index.html", {"info":info.get("title"), "video_id":video_id})
    
    return render(request, "index.html")
        
def download(request, video_id):
    for file in os.listdir('downloads'):
        if file.startswith(video_id):
            filepath = os.path.join('downloads', file)
            f = open(filepath, 'rb') 
            return FileResponse(f, as_attachment=True, filename=file)
    return HttpResponse("Arquivo não encontrado.", status=404)
    