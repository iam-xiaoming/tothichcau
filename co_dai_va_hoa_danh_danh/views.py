from django.shortcuts import render, redirect
from .utils import Artconvert
import pygame as pg

# Create your views here.
def run(request):
    app = Artconvert()
    app.run()
    return redirect('home')