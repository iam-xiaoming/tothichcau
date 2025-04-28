from django.urls import path
from . import views

urlpatterns = [
    path('api/category/', views.api_category, name='api-category')
]