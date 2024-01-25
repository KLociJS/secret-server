from rest_framework import serializers
from .models import Secret

def is_remaining_views_valid(value):
    if value < 1:
        raise serializers.ValidationError(
            'Remaining views must be greater than 0.'
        )
    
class SecretSerializer(serializers.ModelSerializer):
    remainingViews = serializers.IntegerField(
        validators=[is_remaining_views_valid]
    )
    class Meta:
        model = Secret
        fields = ('__all__')
