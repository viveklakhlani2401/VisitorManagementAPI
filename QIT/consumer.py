import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from .models import QitUserlogin,QitNotificationmaster
from datetime import datetime
from django.utils import timezone
from QIT.Views import common
class SocketConsumer(AsyncWebsocketConsumer):
    connections = []

    async def send_initial_data(self,id):
        users = await sync_to_async(list)(QitUserlogin.objects.values())
        today = timezone.now().date()
        # norifications = await sync_to_async(list)(QitNotificationmaster.objects.filter(
        #     receiver_user_id=id,
        #     chk_status='P',
        #     n_date_time__date=today 
        # ))
        notifications = await sync_to_async(list)(QitNotificationmaster.objects.filter(
            receiver_user_id=id,
            # chk_status='P',
            n_date_time__date=today
        ).values('transid', 'notification_text', 'n_date_time', 'chk_status'))
        for notification in notifications:
            if 'n_date_time' in notification:
                notification['n_date_time'] = common.time_since(notification['n_date_time'])
        # notifications = self.serialize_notifications(notifications)

        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            # 'users': users,
            'notification': notifications
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
        await self.send_initial_data(self.user_id)

    async def disconnect(self, close_code):
        if hasattr(self, 'custom_groups'):
            for group in self.custom_groups:
                await self.channel_layer.group_discard(f"user_{group}", self.channel_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def new_notification(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))

    async def send_message(self, event):
        text = event['text']
        await self.send(text_data=json.dumps(text))
