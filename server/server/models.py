from django.db import models
from shortuuid.django_fields import ShortUUIDField

class Secret(models.Model):
    hash = ShortUUIDField(length=16, max_length=16, prefix='secret_', primary_key=True)
    secret_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    remaining_views = models.IntegerField()