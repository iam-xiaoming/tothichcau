from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer
from .models import Category

# Create your views here.
@api_view(['GET'])
def api_category(request):
    context = Category.objects.all()
    serializer = CategorySerializer(context, many=True)
    return Response({
        'success': True,
        'categories': serializer.data
    }, status=200)