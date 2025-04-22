from rest_framework import serializers

class SearchQuerySerializer(serializers.Serializer):
    query = serializers.CharField()
    offset = serializers.IntegerField(default=0)
    limit = serializers.IntegerField(default=5)