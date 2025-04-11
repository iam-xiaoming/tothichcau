from django.shortcuts import render
from django.http import FileResponse
import os
from django.conf import settings

# Create your views here.
def so_close_so_far(request):
    img_url = 'thanks/img/image.png'
    audio_url = 'thanks/audio/lc2.mp3'
    context = {
        'img_url': img_url,
        'audio_url': audio_url
    }
    return render(request, 'thanks/thanks.html', context)


def memorable(request):
    return render(request, 'thanks/memorable.html')


def word_apart(request):
    img_url = 'thanks/img/img2.JPG'
    audio_url = 'thanks/audio/lc5.mp3'
    context = {
        'img_url': img_url,
        'audio_url': audio_url
    }
    return render(request, 'thanks/thanks.html', context)


def recall(request):
    img_url = 'thanks/img/img1.JPG'
    audio_url = 'thanks/audio/recall.mp3'
    context = {
        'img_url': img_url,
        'audio_url': audio_url
    }
    return render(request, 'thanks/thanks.html', context)


def thanks(request):
    img_url = 'thanks/img/thanks.jpg'
    audio_url = 'thanks/audio/main.mp3'
    context = {
        'img_url': img_url,
        'audio_url': audio_url
    }
    print('Thank you because of reading my message! I made it special for you!....................................................................................................................................................................................................................................')
    return render(request, 'thanks/thanks.html', context)