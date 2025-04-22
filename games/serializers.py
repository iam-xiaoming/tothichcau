from rest_framework import serializers
from games.models import Game

class GameSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = (
            "id",
            "name",
            "discounted_price",
            'image',
            'categories'
        )
        
    def get_discounted_price(self, obj):
        return obj.discounted_price
    
    def get_categories(self, obj):
        return [{'id': category.id, 'name': category.name} for category in obj.categories.all()]
