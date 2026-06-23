from django.db import models
from user_app.models import User
from profile_app.models import Profile

MONTHS_UA = {
    1: "січня",
    2: "лютого",
    3: "березня",
    4: "квітня",
    5: "травня",
    6: "червня",
    7: "липня",
    8: "серпня",
    9: "вересня",
    10: "жовтня",
    11: "листопада",
    12: "грудня",
}

class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    name = models.CharField(max_length=30, null=True, blank=True)
    is_group = models.BooleanField(default=False)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to='media/chat_app/group_avatars', null=True, blank=True)

    def __str__(self):
        return self.name if self.name else f"Chat {self.id}"
    

class Message(models.Model):
    text = models.TextField(null=True, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='messages', null=True, blank=True)
    readers = models.ManyToManyField(to=User, related_name='read_messages')
    
    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"
    
    def format_ua_date(self):
        return f"{self.created_at.day} {MONTHS_UA[self.created_at.month]} {self.created_at.year}"
    
class MessageImage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="media/chat_app/message_images")

    def get_json(self):
        return {
            'id': self.id,
            'image': self.image.url
        }
