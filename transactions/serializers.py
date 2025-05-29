from rest_framework import serializers
from cart.models import Transaction

class TransactionHistorySerializer(serializers.ModelSerializer):
    game_name = serializers.SerializerMethodField()
    dlc_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('id', 'game_name', 'dlc_name', 'created_at', 'total_amount', 'status')

    def get_game_name(self, obj):
        return obj.game.name if obj.game else None

    def get_dlc_name(self, obj):
        return obj.dlc.name if obj.dlc else None