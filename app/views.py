from django.shortcuts import render
from yt_dlp import YoutubeDL
from django.http import FileResponse, HttpResponse
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def index(request):
    if request.method == "POST":
        url = request.POST.get("url")
        
        cookies_url = os.getenv("COOKIES_URL")
        
        response = requests.get(cookies_url)

        # Decodifica o conteúdo para texto UTF-8
        text = response.content.decode('utf-8')

        # Remove BOM UTF-8 se existir
        text = text.lstrip('\ufeff')

        import re
        lines = text.splitlines()
        new_lines = []

        for line in lines:
            if line.startswith('#') or line.strip() == '':
                new_lines.append(line)  # mantém comentários e linhas vazias
            else:
                # substitui 2 ou mais espaços por tab
                line_fixed = re.sub(r' {2,}', '\t', line)
                new_lines.append(line_fixed)

        corrected_text = '\n'.join(new_lines)

        # Salva o arquivo corrigido para o yt-dlp
        with open('cookies.txt', 'w', encoding='utf-8') as f:
            f.write(corrected_text)

        print("Cookies baixados e corrigidos com sucesso.")
        
        ydl_opts = {
            'cookiefile': 'cookies.txt',
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
    