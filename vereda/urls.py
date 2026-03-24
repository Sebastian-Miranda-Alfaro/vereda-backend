"""
URL configuration for vereda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Importamos las vistas que nos regala la librería para generar tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usuarios.views import registrar_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conectamos las rutas de tu API:
    path('api/', include('comunidad.urls')),
    # --- RUTAS DE AUTENTICACIÓN ---
    # Esta es la ruta para hacer "Login" y obtener el token
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Esta ruta sirve para renovar el token cuando caduca (seguridad extra)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/registro/', registrar_usuario, name='registro_api'),
]
