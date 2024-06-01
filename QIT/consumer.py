import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from .models import QitUserlogin


class ChatConsumer(AsyncWebsocketConsumer):
    connections = []
    async def send_initial_data(self):
        print("====")
        users = await sync_to_async(list)(QitUserlogin.objects.values())
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'users': users
        }))

    async def connect(self):
        self.group_name = 'users_group'
        query_string = self.scope['query_string'].decode()
        params = query_string.split('&')
        user_param = [param for param in params if param.startswith('user=')]
        self.custom_groups = []

        if user_param:
            self.user_id = user_param[0].split('=')[1]
            self.custom_groups.append(self.user_id)
            await self.channel_layer.group_add(f"user_{self.user_id}", self.channel_name)
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_initial_data()

    async def disconnect(self, close_code):
        if hasattr(self, 'custom_groups'):
            for group in self.custom_groups:
                await self.channel_layer.group_discard(f"user_{group}", self.channel_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def send_info_to_custom_group(self, user_ids, event):
        text = event['text']
        for user_id in user_ids:
            await self.channel_layer.group_send(
                f"user_{user_id}",
                {
                    'type': 'send.message',
                    'text': text,
                }
            )

    async def send_message(self, event):
        text = event['text']
        await self.send(text_data=json.dumps(text))
