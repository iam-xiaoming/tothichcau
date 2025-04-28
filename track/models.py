from django.db import models

# Create your models here.

class UserInteraction(models.Model):
    user_id = models.CharField(max_length=255, editable=False)
    item_id = models.CharField(max_length=255, editable=False)
    timestamp = models.BigIntegerField(editable=False)
    event_type = models.CharField(max_length=255, editable=False)

    def __str__(self):
        return f"{self.user_id} {self.item_id} {self.event_type}"
