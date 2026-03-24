from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PeticionOracion, LecturaEnVivo
from .serializers import PeticionOracionSerializer, LecturaEnVivoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# --- VISTA 1: El muro de Oraciones ---
class PeticionOracionListCreate(generics.ListCreateAPIView):
    queryset = PeticionOracion.objects.all().order_by('-fecha_creacion')
    serializer_class = PeticionOracionSerializer
    permission_classes = [IsAuthenticated] # Candado activado
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)
        
# ListCreateAPIView hace la magia de darnos dos funciones a la vez:
# 1. Leer todas las peticiones (GET)
# 2. Crear una nueva petición (POST)
class LecturaEnVivoListCreate(generics.ListCreateAPIView):
    queryset = LecturaEnVivo.objects.all().order_by('-ultima_actividad')
    serializer_class = LecturaEnVivoSerializer
    permission_classes = [IsAuthenticated]
    

    def perform_create(self, serializer):
        # 1. Buscamos si el usuario ya tiene una lectura activa en la tabla
        lectura_existente = LecturaEnVivo.objects.filter(usuario=self.request.user).first()
        
        if lectura_existente:
            # 2. Si ya existe, hacemos un UPDATE solo de los campos necesarios
            lectura_existente.libro = serializer.validated_data.get('libro')
            lectura_existente.capitulo = serializer.validated_data.get('capitulo')
            lectura_existente.save()
        else:
            # 3. Si no existe (es su primera vez), hacemos el INSERT normal
            serializer.save(usuario=self.request.user)
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'lectura_global', # El nombre del grupo en tu consumers.py
            {
                'type': 'enviar_actualizacion', # El nombre de la función que recibe el mensaje
                'datos': {
                    'usuario_nombre': self.request.user.username,
                    'libro': serializer.validated_data.get('libro'),
                    'capitulo': serializer.validated_data.get('capitulo')
                }
            }
        )

class IncrementarOracionView(APIView):
    permission_classes = [IsAuthenticated] # ¡Con candado!

    def post(self, request, pk):
        # Buscamos la petición por su ID (pk = primary key)
        peticion = get_object_or_404(PeticionOracion, pk=pk)
        
        # Le sumamos 1 al contador
        peticion.oraciones_recibidas += 1
        peticion.save()
        
        return Response({'mensaje': '¡Contador actualizado!'})