from django.urls import path, include
from .views import PeticionOracionListCreate,LecturaEnVivoListCreate,IncrementarOracionView,VersiculoCompartidoViewSet
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'compartidos', VersiculoCompartidoViewSet, basename='compartido')

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
    #Rutas para eliminar
    path('subrayados/<str:libro>/<int:capitulo>/<int:versiculo>/', views.eliminar_subrayado),
    path('notas/<str:libro>/<int:capitulo>/<int:versiculo>/', views.eliminar_nota),
    # RUTA PARA ELIMINAR DEL FEED
    path('compartidos/<int:compartido_id>/', views.eliminar_compartido),
    
    path('', include(router.urls)),
]