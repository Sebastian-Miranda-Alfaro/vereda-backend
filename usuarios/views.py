from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import json

User = get_user_model()

# Inicializamos el cliente de OpenAI de forma segura
client = OpenAI(api_key=settings.OPENAI_API_KEY)

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