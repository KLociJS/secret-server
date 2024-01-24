from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializer import SecretSerializer
from .models import Secret

@api_view(['POST'])
def post_secret(request):
    if request.method == 'POST':

        serializer = SecretSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET'])
def get_secret_list(request):
    if request.method == 'GET':
        secrets = Secret.objects.all()
        serializer = SecretSerializer(secrets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@renderer_classes([JSONRenderer, XMLRenderer])
def get_secret(request, hash):
    try:
        secret = Secret.objects.get(pk=hash)

        if secret.is_available():
            serializer = SecretSerializer(secret)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Secret not available'}, status=status.HTTP_404_NOT_FOUND)
    
    except Secret.DoesNotExist:
        return Response({'error': 'Secret not found'}, status=status.HTTP_404_NOT_FOUND)
    