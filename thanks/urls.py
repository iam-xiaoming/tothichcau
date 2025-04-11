from django.urls import path
from .views import thanks, so_close_so_far, memorable, recall, word_apart

urlpatterns = [
    path('', thanks, name='thanks'),
    path('so_close_so_far/', so_close_so_far, name='so_close_so_far'),
    path('memorable/', memorable, name='memorable'),
    path('recall/', recall, name='recall'),
    path('world_apart/', word_apart, name='world_apart')
]