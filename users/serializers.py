from rest_framework import serializers
from games.models import Game
from keys.models import Key
from cart.models import Transaction
from .models import UserGame

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id',)

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'image')

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('key',)

class UserGameSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    transaction = TransactionSerializer()
    key = KeySerializer()
    
    class Meta:
        model = UserGame
        fields = ('game', 'transaction', 'key')
