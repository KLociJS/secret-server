from django.db import models
from shortuuid.django_fields import ShortUUIDField
from datetime import datetime, timedelta
from encrypted_model_fields.fields import EncryptedTextField


class Secret(models.Model):
    hash = ShortUUIDField(
        length=16,
        max_length=23,
        prefix='secret_',
        primary_key=True
    )
    secret_text = EncryptedTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_in = models.IntegerField()
    remaining_views = models.IntegerField()

    def is_available(self):

        expiration_date = self.created_at + timedelta(minutes=self.expires_in)

        has_no_expiration = self.expires_in == 0
        is_not_expired = (
            expiration_date.timestamp() > datetime.now().timestamp()
        )
        has_remaining_views = self.remaining_views > 0

        is_available = has_remaining_views and (
            is_not_expired or has_no_expiration)

        if is_available:
            self.remaining_views -= 1
            self.save()

        return is_available
