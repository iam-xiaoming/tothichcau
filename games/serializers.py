from rest_framework import serializers
from games.models import Game
from game_features.serializers import GameImageReviewSerializer, GameVideoReviewSerializer

class GameSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    image_reviews = serializers.SerializerMethodField()
    video_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = (
            "id",
            "name",
            "discounted_price",
            'image',
            'categories',
            'image_reviews',
            'video_reviews'
        )
        
    def get_discounted_price(self, obj):
        return obj.discounted_price
    
    def get_categories(self, obj):
        return [{'id': category.id, 'name': category.name} for category in obj.categories.all()]
    
    def get_image_reviews(self, obj):
        reviews = obj.game_image_reviews.all()
        return GameImageReviewSerializer(reviews, many=True).data
    
    def get_video_reviews(self, obj):
        reviews = obj.game_video_reviews.all()
        return GameVideoReviewSerializer(reviews, many=True).data
    
    
    
class DLCSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    image_reviews = serializers.SerializerMethodField()
    video_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = (
            "id",
            "name",
            "discounted_price",
            'image',
            'categories',
            'image_reviews',
            'video_reviews'
        )
        
    def get_discounted_price(self, obj):
        return obj.discounted_price
    
    def get_categories(self, obj):
        return [{'id': category.id, 'name': category.name} for category in obj.game.categories.all()]
    
    def get_image_reviews(self, obj):
        reviews = obj.dlc_image_reviews.all()
        return GameImageReviewSerializer(reviews, many=True).data
    
    def get_video_reviews(self, obj):
        reviews = obj.dlc_video_reviews.all()
        return GameVideoReviewSerializer(reviews, many=True).data
