from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from elasticsearch_dsl import Q
from search.serializers import SearchQuerySerializer
from games.documents import GameDocument, DLCDocument
from games.serializers import GameSerializer, DLCSerializer
from games.models import Game, DLC
from users.models import UserGame
from users.documents import UserGameDocument
from users.serializers import UserGameSerializer
from users.documents import UserGameDocument
from transactions.documents import TransactionDocument
from transactions.serializers import TransactionHistorySerializer
from cart.models import Transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication 

# Create your views here.
class GameSearchAPIView(APIView):
    # define document and serializer
    game_serializer_class = GameSerializer
    dlc_serializer_class = DLCSerializer
    game_document_class = GameDocument
    dlc_document_class = DLCDocument
    query_serializer_class = SearchQuerySerializer

    def elasticsearch_query_expression(self, query):
        return Q(
            "bool",
            should=[
                # search base on 3 methods
                # match name with boost = 2
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
            # just need to match one in both of 3 methods
            minimum_should_match=1
        )

    def get(self, request):
        # take query from url
        search_query = self.query_serializer_class(data=request.GET.dict())
        if not search_query.is_valid():
            return DRFResponse(f"Validation error: {search_query.errors}", status=status.HTTP_400_BAD_REQUEST)

        query_data = search_query.data
        
        # searching
        try:
            q = self.elasticsearch_query_expression(query_data["query"])
            game_search = self.game_document_class.search().query(q)
            dlc_search = self.dlc_document_class.search().query(q)

            # searching games
            game_search = game_search[query_data["offset"]: query_data["offset"] + query_data["limit"]]
            game_response = game_search.execute()
            
            # searching dlcs
            dlc_search = dlc_search[query_data["offset"]: query_data["offset"] + query_data["limit"]]
            dlc_response = dlc_search.execute()
            
            # serializer results - hit is document
            game_ids = [hit.meta.id for hit in game_response.hits]
            games = Game.objects.filter(id__in=game_ids)
            
            dlc_ids = [hit.meta.id for hit in dlc_response.hits]
            dlcs = DLC.objects.filter(id__in=dlc_ids)
            
            game_serializer = self.game_serializer_class(games, many=True)
            dlc_serializer = self.dlc_serializer_class(dlcs, many=True)
            
            games_data = [{'type': 'game', **item} for item in game_serializer.data]
            dlcs_data = [{'type': 'dlc', **item} for item in dlc_serializer.data]

            data = {
                'items': games_data + dlcs_data
            }
            
            return DRFResponse(data, status=status.HTTP_200_OK)
        
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
        
        
class TransactionHistorySearchAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    serializer_class = TransactionHistorySerializer
    document_class = TransactionDocument
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
            
            transaction_ids = [hit.meta.id for hit in response.hits]
            
            
            transactions = Transaction.objects.filter(user=request.user, id__in=transaction_ids)
            
            serializer = self.serializer_class(transactions, many=True)
            
            return DRFResponse(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return DRFResponse(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)