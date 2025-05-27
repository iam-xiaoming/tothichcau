import socket
import requests
import re
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random
import string

def generate_stream_key():
    """Sinh stream_key ngẫu nhiên với 32 ký tự."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

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
    Tạo stream_key và trả về trang setup livestream.
    Stream_key được sinh một lần và truyền vào template.
    """
    stream_key = generate_stream_key()
    context = {
        "server_ip": "47.130.87.247",  # IP tĩnh đã xác nhận
        "stream_key": stream_key,
    }
    return render(request, "livestream/stream_setup.html", context)


@login_required
def check_stream(request):
    """
    Kiểm tra trạng thái stream dựa trên stream_key từ query parameter.
    """
    stream_key = request.GET.get("streamKey")
    if not stream_key or not re.match(r'^[a-zA-Z0-9_-]+$', stream_key):
        return JsonResponse({"status": "error", "detail": "Stream key không hợp lệ"})

    try:
        res = requests.get("http://47.130.87.247:8080/stat", timeout=5)
        res.raise_for_status()
        text = res.text
        print("DEBUG TEXT:", text[:500])

        if stream_key in text:
            return JsonResponse({"status": "connected"})
        else:
            return JsonResponse({"status": "disconnected", "detail": "Stream chưa được đẩy qua RTMP"})
    except requests.RequestException as e:
        return JsonResponse({"status": "error", "detail": f"Lỗi kết nối server: {str(e)}"})


@login_required
def livestream(request):
    """
    Trang xem livestream theo stream_key.
    Hiển thị player chơi HLS stream (m3u8).
    """
    stream_key = request.GET.get("streamKey")
    title = request.GET.get("title", "Livestream của bạn")

    if not stream_key or not re.match(r'^[a-zA-Z0-9_-]+$', stream_key):
        return render(request, "livestream/livestream.html", {
            "stream_key": stream_key,
            "title": "Lỗi: Stream key không hợp lệ hoặc thiếu",
            "stream_url": ""
        })

    stream_url = f"http://47.130.87.247:8080/live/{stream_key}/index.m3u8"
    return render(request, "livestream/livestream.html", {
        "stream_key": stream_key,
        "title": title,
        "stream_url": stream_url
    })