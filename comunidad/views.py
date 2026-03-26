from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics, permissions,viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PeticionOracion, LecturaEnVivo, PreguntaDuda, NotaPersonal, Subrayado, VersiculoCompartido
from .serializers import PeticionOracionSerializer, LecturaEnVivoSerializer, PreguntaDudaSerializer, NotaPersonalSerializer, SubrayadoSerializer, VersiculoCompartidoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

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

# 1. FORO DE DUDAS (Todos ven las dudas del capítulo, autenticados preguntan)
class PreguntaDudaListCreate(generics.ListCreateAPIView):
    serializer_class = PreguntaDudaSerializer
    permission_classes = [permissions.IsAuthenticated] # ¡Seguridad activada!

    def get_queryset(self):
        # React nos pedirá las dudas de un libro y capítulo en específico
        queryset = PreguntaDuda.objects.all()
        libro = self.request.query_params.get('libro', None)
        capitulo = self.request.query_params.get('capitulo', None)
        
        if libro and capitulo:
            queryset = queryset.filter(libro=libro, capitulo=capitulo)
        return queryset.order_by('-fecha_creacion') # Las más nuevas primero

    def perform_create(self, serializer):
        # Asigna automáticamente al usuario que hizo la petición (basado en su Token)
        serializer.save(usuario=self.request.user)


# 2. NOTAS PERSONALES (Privadas, solo el dueño las ve)
class NotaPersonalListCreate(generics.ListCreateAPIView):
    serializer_class = NotaPersonalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # MAGIA DE PRIVACIDAD: Filtramos para que solo devuelva las notas del usuario actual
        return NotaPersonal.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


# 3. SUBRAYADOS (Privados, para que regresen al recargar la app)
class SubrayadoListCreate(generics.ListCreateAPIView):
    serializer_class = SubrayadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo devolvemos los subrayados de quien lo está pidiendo
        return Subrayado.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


# 4. VERSÍCULOS COMPARTIDOS (El Feed público de 24 horas)
class VersiculoCompartidoViewSet(viewsets.ModelViewSet):
    serializer_class = VersiculoCompartidoSerializer

    # Permisos: Cualquiera puede VER (GET), pero solo logueados pueden PUBLICAR (POST)
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # MAGIA DE TIEMPO: Calculamos la hora de ayer, y solo devolvemos los que sean más nuevos
        hace_24_horas = timezone.now() - timedelta(hours=24)
        return VersiculoCompartido.objects.filter(fecha_creacion__gte=hace_24_horas).order_by('-fecha_creacion')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)