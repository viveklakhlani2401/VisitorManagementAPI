import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from .models import QitUserlogin,QitNotificationmaster,QitVisitorinout
from datetime import datetime
from django.utils import timezone
from QIT.serializers import QitVisitorinoutGETSerializer
from QIT.Views import common
class SocketConsumer(AsyncWebsocketConsumer):
    connections = []

    # Semd initially data
    # async def send_initial_data(self,id,cmpid):
    async def send_initial_data(self):
        # users = await sync_to_async(list)(QitUserlogin.objects.values())
        # today = timezone.now().date()
        # norifications = await sync_to_async(list)(QitNotificationmaster.objects.filter(
        #     receiver_user_id=id,
        #     chk_status='P',
        #     n_date_time__date=today 
        # ))

        # Visitor data
        # visitors = await sync_to_async(list)(
        # QitVisitorinout.objects.filter(cmptransid=cmpid)
        #     .select_related('cmpdepartmentid', 'visitortansid')  # Prefetch related fields
        #     .order_by('-checkintime', '-entrydate')
        # )

        # # Function to serialize data synchronously
        # def serialize_visitors(visitors):
        #     serializer = QitVisitorinoutGETSerializer(visitors, many=True)
        #     return serializer.data

        # # Serialize visitors data in a synchronous context
        # serialized_data = await sync_to_async(serialize_visitors)(visitors)

        # # Print or use the serialized data
        # print(serialized_data)


        # notification data
        # notifications = await sync_to_async(list)(QitNotificationmaster.objects.filter(
        #     receiver_user_id=id,
        #     # chk_status='P',
        #     n_date_time__date=today
        # ).values('transid', 'notification_text', 'n_date_time', 'chk_status'))
        # for notification in notifications:
        #     if 'n_date_time' in notification:
        #         notification['n_date_time'] = common.time_since(notification['n_date_time'])
        
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            # 'users': users,
            # 'visitors': serialized_data,
            # 'notification': notifications
        }))
    # End initially data
    
    # Connection
    async def connect(self):
        self.group_name = 'users_group'
        query_string = self.scope['query_string'].decode()
        params = query_string.split('&')
        user_param = [param for param in params if param.startswith('user=')]
        self.custom_groups = []
        cmp_param = [param for param in params if param.startswith('cmp=')]

        if user_param:
            self.user_id = user_param[0].split('=')[1]
            self.cmp_id = cmp_param[0].split('=')[1]
            self.custom_groups.append(self.user_id)
            await self.channel_layer.group_add(f"user_{self.user_id}_cmp{self.cmp_id}", self.channel_name)
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # await self.send_initial_data(self.user_id,self.cmp_id)
    # End Connection

    # Disconnection   
    async def disconnect(self, close_code):
        if hasattr(self, 'custom_groups'):
            for group in self.custom_groups:
                await self.channel_layer.group_discard(f"user_{group}", self.channel_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    # End Disconnection

    # Handle New notifications
    async def new_notification(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))
    # End Handle new notifications
        
    # Handle New visitor
    async def new_visitor(self, event):
        visitor = event['visitor']
        await self.send(text_data=json.dumps({
            'type': 'update_visitor',
            'visitor': visitor
        }))
    # End Handle new notifications
    
    async def send_message(self, event):
        text = event['text']
        await self.send(text_data=json.dumps(text))

    # Send visitors
    async def handle_send_visitor_event(self, data):
        visitors = await sync_to_async(list)(
        QitVisitorinout.objects.filter(cmptransid=data)
            .select_related('cmpdepartmentid', 'visitortansid')  # Prefetch related fields
            .order_by('-checkintime', '-entrydate')
        )

        # Function to serialize data synchronously
        def serialize_visitors(visitors):
            serializer = QitVisitorinoutGETSerializer(visitors, many=True)
            return serializer.data

        # Serialize visitors data in a synchronous context
        serialized_data = await sync_to_async(serialize_visitors)(visitors)
        
        # Send back the response
        await self.send(text_data=json.dumps({
            'type': 'visitors',
            'visitors': serialized_data
        }))
    # End Visitor

    # Send Notifications
    async def handle_send_notification_event(self, data):
        today = timezone.now().date()
        notifications = await sync_to_async(list)(QitNotificationmaster.objects.filter(
            receiver_user_id=data,
            n_date_time__date=today
        ).values('transid', 'notification_text', 'n_date_time', 'chk_status'))
        for notification in notifications:
            if 'n_date_time' in notification:
                notification['n_date_time'] = common.time_since(notification['n_date_time'])
        
        # Send back the response
        await self.send(text_data=json.dumps({
            'type': 'notifications',
            'notification': notifications
        }))
    # End Notifications

    # Handle new events by client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json.get('type')

        if event_type == 'send_visitors':
            data = text_data_json.get('cmpid')
            await self.handle_send_visitor_event(data)
        elif event_type == 'send_notifications':
            data = text_data_json.get('usrid')
            await self.handle_send_notification_event(data)
        else:
            # Handle other types of events
            pass
    # End Handle new events by client