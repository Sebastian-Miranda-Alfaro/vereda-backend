from rest_framework import serializers
from .models import PeticionOracion, LecturaEnVivo

class PeticionOracionSerializer(serializers.ModelSerializer):
    # Este pequeño truco extrae el nombre del usuario en texto, 
    # para que el JSON no nos devuelva solo un número de ID aburrido.
    autor_nombre = serializers.ReadOnlyField(source='autor.username')

    class Meta:
        model = PeticionOracion
        # Aquí definimos exactamente qué columnas de la base de datos queremos enviar al celular
        fields = ['id', 'autor_nombre', 'titulo', 'descripcion', 'fecha_creacion', 'oraciones_recibidas']

class LecturaEnVivoSerializer(serializers.ModelSerializer):
    # Extraemos el nombre del usuario para que la app sepa quién es
    usuario_nombre= serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = LecturaEnVivo
        fields = ['id', 'usuario_nombre', 'libro', 'capitulo', 'ultima_actividad']