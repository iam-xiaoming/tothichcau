# livestream/views.py

from django.shortcuts import render
from django.http import JsonResponse
import socket, requests
import re

def get_server_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def stream_setup(request):
    if "stream_key" not in request.session:
        import random, string
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        request.session["stream_key"] = key

    context = {
        "server_ip": get_server_ip(),
        "stream_key": request.session["stream_key"],
    }
    return render(request, "livestream/stream_setup.html", context)


def check_stream(request):
    stream_key = request.GET.get("streamKey")
    try:
        r = requests.get("http://localhost:8080/stat")
        if stream_key:
            pattern = re.compile(re.escape(stream_key))
            if pattern.search(r.text):
                return JsonResponse({"status": "connected"})
        return JsonResponse({"status": "disconnected"})
    except Exception as e:
        return JsonResponse({"status": "error", "detail": str(e)})
    
    
def livestream(request):
    stream_key = request.GET.get("streamKey")
    title = request.GET.get("title", "Livestream của bạn")

    # URL video stream giả định (có thể thay đổi tuỳ config của bạn)
    stream_url = f"http://localhost:8080/live/{stream_key}.m3u8" if stream_key else ""

    context = {
        "stream_key": stream_key,
        "title": title,
        "stream_url": stream_url,
    }
    return render(request, "livestream/livestream.html", context)