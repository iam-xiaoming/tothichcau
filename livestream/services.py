import requests
from django.conf import settings

def create_livepeer_stream(stream_name):
    url = "https://livepeer.studio/api/stream"
    headers = {
        "Authorization": f"Bearer {settings.LIVEPEER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "name": stream_name,
        "profiles": [
            {
                "name": "720p",
                "bitrate": 2000000,
                "fps": 30,
                "width": 1280,
                "height": 720,
            },
            {
                "name": "480p",
                "bitrate": 1000000,
                "fps": 30,
                "width": 854,
                "height": 480,
            },
        ],
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.HTTPError as err:
        print("HTTP error:", err.response.json())
        raise