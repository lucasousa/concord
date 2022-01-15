import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import User

from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = self.scope["url_route"]["kwargs"]["room_uuid"]
        self.room_group_name = f"room_{self.room}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print("=========", data)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "receive_message", **data},
        )

    async def receive_message(self, event):
        data = event.copy()
        del data["type"]
        message = await self.save_message(**data)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "new_message",
                    "data": message.to_dict(),
                }
            )
        )

    @sync_to_async
    def save_message(self, useruuid, roomuuid, message):
        user = User.objects.get(uuid=useruuid)
        room = Room.objects.get(uuid=roomuuid)
        return Message.objects.create(user=user, room=room, text=message)
