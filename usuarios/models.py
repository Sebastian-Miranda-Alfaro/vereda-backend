from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UsuarioJoven(AbstractUser):
    # Django ya incluye username, email, password, etc.
    avatar = models.ImageField(upload_to='avatares/', null=True, blank=True)
    racha_lectura = models.IntegerField(default=0)
    bio = models.TextField(max_length=150, blank=True)
    def __str__(self):
        return self.username

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_evento = models.DateTimeField() # Guarda fecha y hora exacta
    imagen_url = models.URLField(max_length=500, blank=True, null=True, help_text="Link de la imagen del flyer")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Esto hace que en el panel de admin se vea el nombre del evento y no "Objeto 1"
        return f"{self.titulo} - {self.fecha_evento.strftime('%d/%m/%Y')}"