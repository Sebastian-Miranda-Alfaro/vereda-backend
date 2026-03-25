from django.urls import path
from .views import PeticionOracionListCreate,LecturaEnVivoListCreate,IncrementarOracionView
from . import views

urlpatterns = [
    # Cuando alguien visite esta ruta, se ejecutará la vista que acabamos de crear
    path('oraciones/', PeticionOracionListCreate.as_view(), name='lista_oraciones'),
    path('lecturas/', LecturaEnVivoListCreate.as_view(), name='lista_lecturas'),
    path('oraciones/<int:pk>/orar/', IncrementarOracionView.as_view()),
    # GET: Trae las dudas del capítulo / POST: Crea una duda nueva
    path('dudas/', views.PreguntaDudaListCreate.as_view(), name='dudas-lista'),
    
    # GET: Trae MIS notas / POST: Guarda una nota privada
    path('notas/', views.NotaPersonalListCreate.as_view(), name='notas-lista'),
    
    # GET: Trae MIS colores / POST: Guarda un versículo subrayado
    path('subrayados/', views.SubrayadoListCreate.as_view(), name='subrayados-lista'),
    
    # GET: Trae el feed de 24hrs / POST: Comparte algo con todos
    path('compartidos/', views.VersiculoCompartidoListCreate.as_view(), name='compartidos-lista'),
]