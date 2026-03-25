from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import json
from django.utils import timezone
from .models import Evento

User = get_user_model()

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

# --- 2. NUEVA FUNCIÓN DEL DEVOCIONAL CON IA ---
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def obtener_devocional_diario(request):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        prompt_sistema = """
            Eres un pastor juvenil moderno, sabio y motivador para jóvenes de 13 a 18 años. 
            Tu misión es darles un mensaje de aliento corto para empezar el día.
            Dame un versículo bíblico inspirador en español (cualquier versión moderna como NVI) 
            y un devocional muy corto (menos de 80 palabras) enfocado en adolescentes basado en ese versículo.
            Devuelve la respuesta ESTRICTAMENTE en este formato JSON, sin texto extra:
            {
              "versiculo": "Texto del versículo y referencia (ej. Juan 3:16 NVI)",
              "mensaje": "Texto del devocional corto..."
            }
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": "Dame el devocional de hoy."}
            ],
            temperature=0.7, 
            max_tokens=300 
        )

        json_respuesta_ia = response.choices[0].message.content
        datos_devocional = json.loads(json_respuesta_ia)

        return Response(datos_devocional, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error en OpenAI: {e}")
        return Response({
            'versiculo': 'Filipenses 4:13 NVI',
            'mensaje': '¡Todo lo puedes en Cristo que te fortalece! (Mensaje de respaldo).'
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Solo jóvenes logueados pueden ver los eventos
def obtener_eventos(request):
    # LA MAGIA: Filtramos (filter) los eventos donde la fecha sea MAYOR o IGUAL (gte) a la fecha y hora de este instante (timezone.now)
    # y los ordenamos (order_by) para que el evento más próximo salga primero.
    eventos_activos = Evento.objects.filter(fecha_evento__gte=timezone.now()).order_by('fecha_evento')
    
    # Preparamos la lista para React
    lista_eventos = []
    for evento in eventos_activos:
        lista_eventos.append({
            'id': evento.id,
            'titulo': evento.titulo,
            'descripcion': evento.descripcion,
            'fecha_evento': evento.fecha_evento.isoformat(), # Lo mandamos en formato ISO (ej. 2026-04-15T18:00:00Z) para que la cuenta regresiva de React lo entienda fácil
            'imagen_url': evento.imagen_url
        })
        
    return Response(lista_eventos, status=status.HTTP_200_OK)