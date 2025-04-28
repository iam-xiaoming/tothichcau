from django.urls import path
from . import views

urlpatterns = [
    path('api/interaction/', views.user_interaction_api, name='user-interaction'),
]