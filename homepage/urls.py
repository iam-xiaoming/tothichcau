from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListGameView.as_view(), name='home')
]