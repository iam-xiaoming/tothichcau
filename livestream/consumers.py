import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage
import datetime

@sync_to_async
def save_chat_message(stream_id, username, message):
    ChatMessage.objects.create(
        stream_id=stream_id,
        username=username,
        message=message
    )

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        self.room_group_name = f'chat_{self.stream_id}'

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

    async def receive(self, text_data):
        user = self.scope['user']
        if user.is_anonymous:
            await self.send(text_data=json.dumps({
                'error': 'Bạn cần đăng nhập để bình luận.'
            }))
            return

        data = json.loads(text_data)
        message = data['message']
        username = user.username
        
        await save_chat_message(self.stream_id, username, message)
        
        timestamp = datetime.datetime.now().isoformat()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': timestamp
            }
        )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
        }))
