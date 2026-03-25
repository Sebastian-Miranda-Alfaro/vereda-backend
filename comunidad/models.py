from django.db import models
from django.conf import settings # Esto nos permite el modelo de UsuarioJoven
from django.utils import timezone
from datetime import timedelta

class PeticionOracion(models.Model):
    # Conectamos cada petición con el usuario que la escribió
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='peticiones')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    oraciones_recibidas = models.IntegerField(default=0) # El contador de clics

    def __str__(self):
        return f"{self.titulo} - {self.autor.username}"

class LecturaEnVivo(models.Model):
    # Usamos OneToOneField porque un joven solo puede estar leyendo un capítulo a la vez
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lectura_actual')
    libro = models.CharField(max_length=50) # Ej. "Mateo"
    capitulo = models.IntegerField()
    ultima_actividad = models.DateTimeField(auto_now=True) # Se actualiza solo cada que interactúa

    def __str__(self):
        return f"{self.usuario.username} está leyendo {self.libro} {self.capitulo}"

# 1. FORO DE DUDAS (Por capítulo)
class PreguntaDuda(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libro = models.CharField(max_length=50)
    capitulo = models.IntegerField()
    versiculo = models.IntegerField(null=True, blank=True)
    pregunta = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    resuelta = models.BooleanField(default=False)

    def __str__(self):
        return f"Duda de {self.usuario.username} en {self.libro} {self.capitulo}"


# 2. NOTAS PERSONALES (Privadas, se quedan para siempre)
class NotaPersonal(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libro = models.CharField(max_length=50)
    capitulo = models.IntegerField()
    versiculo = models.IntegerField()
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota de {self.usuario.username} - {self.libro} {self.capitulo}:{self.versiculo}"


# 3. SUBRAYADOS (Para que el color regrese al abrir la app)
class Subrayado(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libro = models.CharField(max_length=50)
    capitulo = models.IntegerField()
    versiculo = models.IntegerField()
    color = models.CharField(max_length=20, default="amarillo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subrayado de {self.usuario.username} - {self.libro} {self.capitulo}:{self.versiculo}"


# 4. VERSÍCULOS COMPARTIDOS (El "Estado" de 24 horas para el Inicio)
class VersiculoCompartido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libro = models.CharField(max_length=50)
    capitulo = models.IntegerField()
    versiculo = models.IntegerField()
    texto_biblico = models.TextField(help_text="El texto literal del versículo")
    nota_publica = models.TextField(help_text="Lo que el usuario opina o reflexiona de este versículo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    @property
    def esta_activo(self):
        return self.fecha_creacion >= timezone.now() - timedelta(hours=24)

    def __str__(self):
        return f"{self.usuario.username} compartió {self.libro} {self.capitulo}:{self.versiculo}"