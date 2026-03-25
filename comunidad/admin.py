from django.contrib import admin
from .models import PeticionOracion, LecturaEnVivo, PreguntaDuda, NotaPersonal, Subrayado, VersiculoCompartido


admin.site.register(PeticionOracion)
admin.site.register(LecturaEnVivo)
admin.site.register(PreguntaDuda)
admin.site.register(NotaPersonal)
admin.site.register(Subrayado)
admin.site.register(VersiculoCompartido)