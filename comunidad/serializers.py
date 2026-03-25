from rest_framework import serializers
from .models import PeticionOracion, LecturaEnVivo , PreguntaDuda, NotaPersonal, Subrayado, VersiculoCompartido

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

# 1. Traductor para el Foro de Dudas
class PreguntaDudaSerializer(serializers.ModelSerializer):
    # Esto es magia: Le mandamos a React el nombre del usuario, no solo su ID numérico
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username') 

    class Meta:
        model = PreguntaDuda
        fields = '__all__'
        # Evitamos que alguien malintencionado mande datos falsos
        read_only_fields = ['usuario', 'fecha_creacion', 'resuelta'] 


# 2. Traductor para Notas Personales
class NotaPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaPersonal
        fields = '__all__'
        read_only_fields = ['usuario', 'fecha_creacion']


# 3. Traductor para Subrayados
class SubrayadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrayado
        fields = '__all__'
        read_only_fields = ['usuario', 'fecha_creacion']


# 4. Traductor para Versículos Compartidos (El feed de 24 hrs)
class VersiculoCompartidoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')
    # ¡Súper útil! Le mandamos a React la foto de perfil del joven para que el muro se vea increíble
    usuario_avatar = serializers.ImageField(source='usuario.avatar', read_only=True) 

    class Meta:
        model = VersiculoCompartido
        fields = '__all__'
        read_only_fields = ['usuario', 'fecha_creacion']