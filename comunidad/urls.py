from django.urls import path
from .views import PeticionOracionListCreate,LecturaEnVivoListCreate,IncrementarOracionView

urlpatterns = [
    # Cuando alguien visite esta ruta, se ejecutará la vista que acabamos de crear
    path('oraciones/', PeticionOracionListCreate.as_view(), name='lista_oraciones'),
    path('lecturas/', LecturaEnVivoListCreate.as_view(), name='lista_lecturas'),
    path('oraciones/<int:pk>/orar/', IncrementarOracionView.as_view()),
]