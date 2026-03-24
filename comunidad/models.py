from django.db import models
from django.conf import settings # Esto nos permite el modelo de UsuarioJoven

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