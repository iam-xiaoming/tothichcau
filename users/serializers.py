from rest_framework import serializers
from games.models import Game, UserGame
from cart.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id',)

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('name',)

class UserGameSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    transaction = TransactionSerializer()
    
    class Meta:
        model = UserGame
        fields = ('game', 'transaction',)
