from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from cart.models import Transaction

@registry.register_document
class TransactionDocument(Document):
    game_name = fields.TextField(attr='game.name')
    dlc_name = fields.TextField(attr='dlc.name')
    
    class Index:
        name = 'transactions'
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
        model = Transaction
        fields = ['id']