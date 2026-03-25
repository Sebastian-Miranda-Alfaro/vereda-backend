from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        # --- EL CAMBIO ESTÁ AQUÍ ---
        # Lo movimos ADENTRO de la función para que Django no se confunda
        User = get_user_model() 
        
        username = 'sebastian' # <--- Pon tu usuario
        email = 'admin@vereda.com'
        password = '123456' # <--- Pon tu contraseña

        if not User.objects.filter(username=username).exists():
            # Usamos los nombres de las variables para evitar errores
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'¡Superusuario {username} creado con éxito en la nube!'))
        else:
            self.stdout.write(self.style.WARNING(f'El usuario {username} ya existe.'))