import socket
import requests
import re
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def get_server_public_ip():
    """
    Lấy IP public của server bằng gọi dịch vụ bên ngoài,
    fallback về IP nội bộ nếu không lấy được.
    """
    try:
        return requests.get("https://api.ipify.org").text
    except requests.RequestException:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)


@login_required
def stream_setup(request):
    """
    Tạo hoặc lấy stream_key trong session.
    Trả về IP server public và stream_key.
    """
    if "stream_key" not in request.session:
        import random
        import string
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        request.session["stream_key"] = key

    context = {
        "server_ip": get_server_public_ip(),
        "stream_key": request.session["stream_key"],
    }
    return render(request, "livestream/stream_setup.html", context)


@login_required
def check_stream(request):
    stream_key = request.GET.get("streamKey")
    try:
        res = requests.get(f"http://{get_server_public_ip()}:8080/stat")
        text = res.text

        print("DEBUG TEXT:", text[:500])
        
        if stream_key in text:
            return JsonResponse({"status": "connected"})
        else:
            return JsonResponse({"status": "disconnected"})
    except Exception as e:
        return JsonResponse({"status": "error", "detail": str(e)})


@login_required
def livestream(request):
    """
    Trang xem livestream theo stream_key.
    Hiển thị player chơi HLS stream (m3u8).
    """
    stream_key = request.GET.get("streamKey")
    title = request.GET.get("title", "Livestream của bạn")

    stream_url = f"http://{get_server_public_ip()}:8080/live/{stream_key}.m3u8" if stream_key else ""

    context = {
        "stream_key": stream_key,
        "title": title,
        "stream_url": stream_url,
    }
    return render(request, "livestream/livestream.html", context)