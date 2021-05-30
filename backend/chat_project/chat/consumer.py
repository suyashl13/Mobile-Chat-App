from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_id

        async_to_sync(self.channel_layer)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        message = text_data['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                type: 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        print("HOST DISCONNECTED.")
