from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from elasticsearch_dsl import Q
from search.serializers import SearchQuerySerializer
from games.documents import GameDocument
from games.serializers import GameSerializer
from games.models import Game, UserGame
from users.documents import UserGameDocument
from users.serializers import UserGameSerializer
from users.documents import UserGameDocument

# Create your views here.
class GameSearchAPIView(APIView):
    serializer_class = GameSerializer
    document_class = GameDocument
    query_serializer_class = SearchQuerySerializer

    def elasticsearch_query_expression(self, query):
        return Q(
            "bool",
            should=[
                Q('multi_match', query=query, fields=['name^2', 'categories.name'], fuzziness='AUTO'),
                Q("match_phrase_prefix", name={"query": query, "boost": 3}),
                Q(
                    "nested",
                    path="categories",
                    query=Q(
                        "match",
                        **{"categories.name": {"query": query}}
                    )
                ),
            ],
            # just need to match one in both of them
            minimum_should_match=1
        )

    def get(self, request):
        # take query from url
        search_query = self.query_serializer_class(data=request.GET.dict())
        if not search_query.is_valid():
            return DRFResponse(f"Validation error: {search_query.errors}", status=status.HTTP_400_BAD_REQUEST)

        query_data = search_query.data
        
        # search
        try:
            q = self.elasticsearch_query_expression(query_data["query"])
            search = self.document_class.search().query(q)

            search = search[query_data["offset"]: query_data["offset"] + query_data["limit"]]
            response = search.execute()
            
            # serializer results - hit is document
            game_ids = [hit.meta.id for hit in response.hits]
            games = Game.objects.filter(id__in=game_ids)
            serializer = self.serializer_class(games, many=True)
            
            return DRFResponse(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return DRFResponse(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserGameSearchAPIView(APIView):
    serializer_class = UserGameSerializer
    document_class = UserGameDocument
    query_serializer_class = SearchQuerySerializer

    def elasticsearch_query_expression(self, query):
        return Q(
            "bool",
            should=[
                Q('match', game_name={'query': query, 'fuzziness': 'AUTO'})
            ]
        )

    def get(self, request):
        if not request.user.is_authenticated:
            return DRFResponse({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Validate query
        search_query = self.query_serializer_class(data=request.GET.dict())
        if not search_query.is_valid():
            return DRFResponse(f"Validation error: {search_query.errors}", status=status.HTTP_400_BAD_REQUEST)

        query_data = search_query.data
        
        # Search
        try:
            q = self.elasticsearch_query_expression(query_data["query"])
            search = self.document_class.search().query(q)
            search = search[query_data["offset"]: query_data["offset"] + query_data["limit"]]
            response = search.execute()
            
            game_ids = [hit.meta.id for hit in response.hits]
            
            
            user_games = UserGame.objects.filter(user=request.user, id__in=game_ids)
            
            serializer = self.serializer_class(user_games, many=True)
            
            return DRFResponse(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return DRFResponse(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)