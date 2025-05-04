from rest_framework import serializers
from .models import GameVideoReview, GameImageReview, Category

class GameImageReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameImageReview
        fields = '__all__'
        
        
class GameVideoReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameVideoReview
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'