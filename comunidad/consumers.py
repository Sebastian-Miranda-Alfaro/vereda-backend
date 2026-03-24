import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LecturaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Cuando un celular se conecta, lo metemos a un grupo llamado 'lectura_global'
        self.room_group_name = 'lectura_global'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept() # Aceptamos la llamada telefónica

    async def disconnect(self, close_code):
        # Cuando el joven cierra la app, lo sacamos del grupo
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Esta función recibe la alerta interna de Django y se la grita a los celulares
    async def enviar_actualizacion(self, event):
        datos = event['datos']
        # Enviamos el JSON por el túnel de WebSocket
        await self.send(text_data=json.dumps({
            'tipo': 'actualizacion_lectura',
            'datos': datos
        }))