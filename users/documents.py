from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from games.models import Game
from .models import UserGame


@registry.register_document
class UserGameDocument(Document):
    game_name = fields.TextField(
        attr="game.name",
        analyzer="custom_edge_ngram",
        fields={"raw": fields.KeywordField()}
    )

    class Index:
        """Elasticsearch index configuration."""
        name = "user_games"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "custom_edge_ngram": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "edge_ngram_filter"]
                    }
                },
                "filter": {
                    "edge_ngram_filter": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 20
                    }
                }
            }
        }

    class Django:
        model = UserGame
        fields = [
            "id",
        ]
        related_models = [Game]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Game):
            return related_instance.game_owned_by_users.all()
        return UserGame.objects.none()