# serializers.py
from rest_framework import serializers
from cart.models import Transaction, Game
from users.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
        
        
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    game = GameSerializer()
    
    class Meta:
        model = Transaction
        fields = '__all__'
