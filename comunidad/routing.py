from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Cuando el celular se conecte a esta dirección, lo atenderá el Locutor
    re_path(r'ws/lecturas/$', consumers.LecturaConsumer.as_asgi()),
]