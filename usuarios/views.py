from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny]) # Permite que cualquiera pueda registrarse sin estar logueado
def registrar_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Por favor, llena todos los campos.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Ese nombre de usuario ya está en uso. ¡Elige otro!'}, status=status.HTTP_400_BAD_REQUEST)

    # create_user es vital porque encripta la contraseña automáticamente
    nuevo_usuario = User.objects.create_user(username=username, password=password)
    return Response({'mensaje': '¡Cuenta creada con éxito!'}, status=status.HTTP_201_CREATED)