from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, DLC
from django.views.generic import DetailView
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .serializers import GameSerializer, DLCSerializer
from users.forms import UserCommentForm
from django.contrib import messages
from games.forms import UserRating

# Create your views here.
class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        game = self.object

        comment_form = UserCommentForm(user=user, game=game)
        scoring_form = UserRating(user=user, game=game)

        context['comment_form'] = comment_form
        context['scoring_form'] = scoring_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        game = self.object
        user = request.user

        comment_form = UserCommentForm(request.POST, user=user, game=game)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            scoring_form = UserRating(request.POST, user=user, game=game, comment=comment)

            if scoring_form.is_valid():
                comment.save()
                scoring_form.save()
                return redirect('game_details', pk=game.pk)
            else:
                print('Scoring Errors', scoring_form.errors)
        else:
            print('Comment Errors', comment_form.errors)

        context = self.get_context_data()
        context['comment_form'] = comment_form
        context['scoring_form'] = scoring_form
        messages.error(request, "There was an error with your comment.")
        return self.render_to_response(context)


class DLCDetailView(DetailView):
    model = DLC
    template_name = 'games/game_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dlc = self.object

        comment_form = UserCommentForm(user=user, dlc=dlc)
        scoring_form = UserRating(user=user, dlc=dlc)

        context['comment_form'] = comment_form
        context['scoring_form'] = scoring_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        dlc = self.object
        user = request.user

        comment_form = UserCommentForm(request.POST, user=user, dlc=dlc)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            scoring_form = UserRating(request.POST, user=user, dlc=dlc, comment=comment)

            if scoring_form.is_valid():
                comment.save()
                scoring_form.save()
                return redirect('dlc-details', pk=dlc.pk)
            else:
                print('Scoring Errors', scoring_form.errors)
        else:
            print('Comment Errors', comment_form.errors)

        context = self.get_context_data()
        context['comment_form'] = comment_form
        context['scoring_form'] = scoring_form
        messages.error(request, "There was an error with your comment.")
        return self.render_to_response(context)
        
           
@api_view(['GET'])
def game_media_review(request, pk):
    try:
        game = Game.objects.get(id=pk)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=HTTP_404_NOT_FOUND)
    
    serializer = GameSerializer(game)
    return Response(serializer.data)


@api_view(['GET'])
def dlc_media_review(request, pk):
    try:
        game = DLC.objects.get(id=pk)
    except DLC.DoesNotExist:
        return Response({'error': 'Game not found'}, status=HTTP_404_NOT_FOUND)
    
    serializer = DLCSerializer(game)
    return Response(serializer.data)