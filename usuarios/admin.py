from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioJoven

class UsuarioJovenAdmin(UserAdmin):
    # Le decimos al panel de administrador que agregue una nueva sección con nuestros campos
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil del Joven', {'fields': ('avatar', 'racha_lectura', 'bio')}),
    )

admin.site.register(UsuarioJoven, UsuarioJovenAdmin)