from channels.generic.websocket import AsyncWebsocketConsumer
import json



class EmergencyRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["user"].id
        self.group_name = f"user_{self.user_id}"

        # Join the user group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the user group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def status_update(self, event):
        # Send the status update to WebSocket
        status = event['status']
        accepted_at = event['accepted_at']

        await self.send(text_data=json.dumps({
            'status': status,
            'accepted_at': accepted_at,
        }))


# class AmbulanceConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.request_id = self.scope['url_route']['kwargs']['request_id']
#         self.room_group_name = f'request_{self.request_id}'

#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         # This method will be called when the driver sends location updates
#         data = json.loads(text_data)
#         location = data['location']

#         # Broadcast the location to the group (i.e., the user)
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'location_update',
#                 'location': location
#             }
#         )

#     # Send location updates to WebSocket
#     async def location_update(self, event):
#         location = event['location']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'location': location
#         }))






# class DriverRequestsConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Join a group for drivers
#         self.group_name = 'driver_requests'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave group
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         # Process incoming data (if needed)
#         pass

#     # Function to send updates to all connected drivers
#     async def send_request_update(self, request_data):
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'send_request',
#                 'request_id': request_data['request_id'],
#                 'user': request_data['user'],
#                 'address': request_data['address'],
#                 'status': request_data['status'],
#             }
#         )

#     async def send_request(self, event):
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'request_id': event['request_id'],
#             'user': event['user'],
#             'address': event['address'],
#             'status': event['status'],
#         }))