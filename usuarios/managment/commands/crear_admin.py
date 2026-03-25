from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'sebastian' # <--- Pon el nombre que quieras
        email = 'admin@vereda.com'
        password = '123456' # <--- PON TU CONTRASEÑA AQUÍ

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Usuario {username} creado con éxito'))
        else:
            self.stdout.write(self.style.WARNING(f'El usuario {username} ya existe'))