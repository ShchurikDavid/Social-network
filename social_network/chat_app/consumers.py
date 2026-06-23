import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string


from .services.load_msg import get_msg_list
from .models import Message, Chat
from profile_app.models import Profile


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat{self.chat_id}'
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        chat = await self.get_chat()

        if chat:
            other_user = await self.get_other_user(chat)
            chat_messages = await self.get_chat_messages_with_date_blocks(chat, 20)
            chat_html = await self.chat_render_to_string(chat, other_user, chat_messages)

            await self.send(
                text_data=json.dumps(
                    {
                        'type': 'connection_confirmation',
                        'chat_messages_html': chat_html,
                        'friends_ids': list([other_user.id]),
                        'message': 'Підключення до чату було успішно встановлено'
                    }
                )
            )

            print(f"Підключення до чату {self.room_group_name} було успішно встановлено")
        else:
            print(f"Чата не существует")
    
    async def receive(self, text_data):
        dict_data = json.loads(text_data)
        message_text = dict_data.get('messageText', '').strip()
        
        if message_text:
            message = await self.save_message(message_text)

            print(1, message.id, message.text)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_chat_message',
                    'message_id': message.id,
                    'input_message': message.text,
                    'message_images': await self.get_images_list(message),
                    'sender': self.scope['user'].username,
                    'my_msg_html': await self.my_msg_to_string(message),
                    'other_msg_html': await self.other_msg_to_string(message),
                }
            )
        
    
    async def send_chat_message(self, event):
        msg_html = None

        if self.scope['user'].username == event['sender']:
            msg_html = event['my_msg_html']
        else: 
            msg_html = event['other_msg_html']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_id': event['message_id'],
            'input_message': event['input_message'],
            'message_images': event['message_images'],
            'sender': event['sender'],
            'msg_html': msg_html
        }))
    
    
    @database_sync_to_async
    def save_message(self, text):
        user = self.scope['user']
        return Message.objects.create(chat_id=self.chat_id, sender=user, text=text)

    @database_sync_to_async
    def chat_render_to_string(self, chat, other_user, chat_messages):
        return render_to_string(
            'chat_app/particals/chat_messages.html',
            {'chat': chat, 'chat_users': chat.users.all(), 'other_user': other_user, 'chat_messages': chat_messages, 'user': self.scope['user']}      
        )
    
    @database_sync_to_async
    def my_msg_to_string(self, messages):
        return render_to_string(
            'chat_app/chat_msg/my_msg.html',
            {'msg': messages, 'user': self.scope['user']}      
        )
    
    @database_sync_to_async
    def other_msg_to_string(self, messages):
        return render_to_string(
            'chat_app/chat_msg/other_msg.html',
            {'msg': messages, 'user': self.scope['user']}      
        )

    @database_sync_to_async
    def get_chat(self):
        try:
            return Chat.objects.get(id=self.chat_id)
        except Chat.DoesNotExist:
            return None

    @database_sync_to_async
    def get_all_messages(self, chat):
        return chat.messages.all().order_by('created_at')
        
    @database_sync_to_async
    def get_other_user(self, chat):
        return chat.users.exclude(id=self.scope['user'].id).first()

    @database_sync_to_async
    def get_chat_messages_with_date_blocks(self, chat, limit):
        messages = chat.messages.all().order_by('-created_at')[:limit]
        messages = reversed(messages)

        return get_msg_list(messages)
    
    @database_sync_to_async
    def get_images_list(self, message):
        images_list = []

        for image in message.images.all():
            images_list.append(image.get_json())

        return images_list 

        