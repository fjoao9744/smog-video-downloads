from celery import shared_task
from yt_dlp import YoutubeDL

@shared_task
def dowload_videos(url):
    ydl_opts = {
        'cookiefile': "cookies.txt",
        'writethumbnail': True,
        'format': 'best',
        'outtmpl': 'static/media/videos/%(id)s.%(ext)s',
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        
    return {
        "id": info.get("id"),
        "title": info.get("title"),
    }
