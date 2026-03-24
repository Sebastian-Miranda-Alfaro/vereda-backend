"""
ASGI config for vereda project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import comunidad.routing # <--- Importamos tus rutas de WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vereda.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # --- NUEVO: Conectamos los WebSockets ---
    "websocket": AuthMiddlewareStack(
        URLRouter(
            comunidad.routing.websocket_urlpatterns
        )
    ),
})
