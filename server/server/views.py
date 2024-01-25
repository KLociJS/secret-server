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

    if request.method == 'POST':
        serializer = SecretSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {'error': 'Invalid input'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET'])
@renderer_classes([JSONRenderer, XMLRenderer, YAMLRenderer])
def get_secret(request, hash):

    if request.method == 'GET':
        secret = get_object_or_404(Secret, hash=hash)

        if secret.is_available():
            serializer = SecretSerializer(secret)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
                headers={'Content-Type': request.accepted_media_type}
            )

        return Response(
            {'error': 'Secret not available'},
            status=status.HTTP_404_NOT_FOUND
        )
