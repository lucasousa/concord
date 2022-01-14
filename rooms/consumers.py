import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Room
from core.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['roomname']
        self.room_group_name = f'room_{self.room}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        useruuid = data['useruuid']
        roomuuid = data['roomuuid']

        await self.save_message(useruuid, roomuuid, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'receive_message',
                'message': message,
                'username': useruuid,
                'room': roomuuid
            }
        )

    async def send_message(self, event):
        print("Aqui no event - ", event)
        await self.send(text_data=json.dumps({
            'type': "send_message",
            'message': event.get('message'),
            'room': event.get('roomuuid'),
            'user': event.get('useruuid'),
        }))

    @sync_to_async
    def save_message(self, useruuid, roomuuid, message):
        user = User.objects.get(uuid=useruuid)
        room = Room.objects.get(uuid=roomuuid)
        Message.objects.create(user=user, room=room, text=message)