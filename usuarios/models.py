from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioJoven(AbstractUser):
    # Django ya incluye username, email, password, etc.
    avatar = models.ImageField(upload_to='avatares/', null=True, blank=True)
    racha_lectura = models.IntegerField(default=0)
    bio = models.TextField(max_length=150, blank=True)

    def __str__(self):
        return self.username