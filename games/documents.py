from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from games.models import Game, Category, DLC

@registry.register_document
class GameDocument(Document):
    discounted_price = fields.FloatField(attr='discounted_price')
    categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer='custom_edge_ngram'),
    })
    
    class Index:
        name = 'games'
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
        model = Game
        fields = ['name', 'image']
        related_models = [Category]
    
    def prepare_categories(self, instance):
        """
        Prepare the categories field by extracting id and name from related Category objects.
        """
        return [
            {'id': category.id, 'name': category.name}
            for category in instance.categories.all()
        ]
        
    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.game_set.all()
        
        

@registry.register_document
class DLCDocument(Document):
    discounted_price = fields.FloatField(attr='discounted_price')
    categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer='custom_edge_ngram'),
    })
    
    class Index:
        name = 'dlcs'
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
        model = DLC
        fields = ['name', 'image']
        related_models = [Category]
    
    def prepare_categories(self, instance):
        """
        Prepare the categories field by extracting id and name from related Category objects.
        """
        return [
            {'id': category.id, 'name': category.name}
            for category in instance.categories.all()
        ]
        
    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.dlc_set.all()