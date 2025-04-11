from django.shortcuts import render

# Create your views here.
def game_details(request):
    return render(request, 'games/game_details.html')