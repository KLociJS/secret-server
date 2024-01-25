from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializer import SecretSerializer
from .models import Secret


@api_view(['POST'])
def post_secret(request):
    """
    Create a new secret.

    Args:
        request (HttpRequest): The HTTP request object.
        request data has to contain the following fields:
            secret (str): The secret to be stored.
            expireAfterViews (int):
            Number of views before the secret is unavailable.
            expireAfter (int): The secret won't be available
            after the given time.
            The value is provided in minutes. 0 means never expires

    Returns:
        Response: Serialized secret or an error message
        if the request data is invalid.
    """

    if request.method == 'POST':
        serializer = SecretSerializer(data=request.data)

        # Check if the serializer is valid.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return 405 if the serializer is not valid.
        return Response(
            {'error': 'Invalid input'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET'])
@renderer_classes([JSONRenderer, XMLRenderer, YAMLRenderer])
def get_secret(request, hash):
    """
    Retrieve a secret based on its hash.

    Args:
        request (HttpRequest): The HTTP request object.
        hash (str): The hash identifying the secret.

    Returns:
        Response: Serialized secret or an error message
        if the secret is not valid or not found.
    """

    if request.method == 'GET':
        secret = get_object_or_404(Secret, hash=hash)

        # Check if the secret is not expired and has remaining views.
        if secret.is_available():
            serializer = SecretSerializer(secret)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
                headers={'Content-Type': request.accepted_media_type}
            )

        # Return 404 if the secret is expired or has no remaining views.
        return Response(
            {'error': 'Secret not available'},
            status=status.HTTP_404_NOT_FOUND
        )
