from rest_framework import serializers
from .models import GameVideoReview, GameImageReview

class GameImageReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameImageReview
        fields = '__all__'
        
        
class GameVideoReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameVideoReview
        fields = '__all__'