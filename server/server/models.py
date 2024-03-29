from django.db import models
from shortuuid.django_fields import ShortUUIDField
from datetime import datetime, timedelta
from encrypted_model_fields.fields import EncryptedTextField


class Secret(models.Model):
    """ Model for storing secrets. """
    hash = ShortUUIDField(
        length=16,
        max_length=23,
        prefix='secret_',
        primary_key=True
    )
    secret = EncryptedTextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    expiresAt = models.IntegerField()
    remainingViews = models.IntegerField()

    def is_available(self):
        """ Checks if the secret is not expired and has remaining views. """
        expiration_date = self.createdAt + timedelta(minutes=self.expiresAt)

        # Check if the secret has no expiration date.
        has_no_expiration = self.expiresAt == 0
        # Check if the secret is not expired.
        is_not_expired = (
            expiration_date.timestamp() > datetime.now().timestamp()
        )
        # Check if the secret has remaining views.
        has_remaining_views = self.remainingViews > 0

        # The secret is available if it has remaining views and is not expired
        is_available = has_remaining_views and (
            is_not_expired or has_no_expiration
        )

        # Decrease the remaining views if the secret is available.
        if is_available:
            self.remainingViews -= 1
            self.save()

        return is_available
