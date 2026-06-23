import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from profile_app.models import Profile


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    online_users = {}

    async def connect(self):
        self.user_id = None
        self.user = self.scope["user"]
        self.group_name = "online_users"
         
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.user_id = str(self.user.id)

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        OnlineStatusConsumer.online_users[self.user_id] = (
            OnlineStatusConsumer.online_users.get(self.user_id, 0) + 1
        )

        if OnlineStatusConsumer.online_users[self.user_id] == 1:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "online_status",
                    "user_id": self.user_id,
                    "status": "online",
                    "it_is_me": int(self.user_id) == int(self.user.id)
                }
            )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "sync_online",
                "online_users": list(OnlineStatusConsumer.online_users.keys())
            }
        )

        print('self.user', self.user, self.user.id, OnlineStatusConsumer.online_users)
    

    async def disconnect(self, code):
        count = OnlineStatusConsumer.online_users.get(self.user_id, 0)

        if count <= 1:
            OnlineStatusConsumer.online_users.pop(self.user_id, None)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "online_status",
                    "user_id": self.user_id,
                    "status": "offline"
                }
            )
        else:
            OnlineStatusConsumer.online_users[self.user_id] = count - 1

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "online_status",
                    "user_id": self.user_id,
                    "status": "online"
                }
            )

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        print('disconnect self.user', self.user, self.user.id, OnlineStatusConsumer.online_users)


    async def online_status(self, event):
        await self.send_status(event["user_id"], event["status"])

    
    async def sync_online(self, event):
        for uid in event["online_users"]:
            await self.send_status(uid, "online")


    async def send_status(self, user_id, status):
        await self.send(text_data=json.dumps({
            "user_id": user_id,
            "status": status,
            "it_is_me": int(user_id) == int(self.user.id)
        }))


from datetime import datetime, timedelta

import jwt
from django.views import View
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class SocketTokenView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        token = jwt.encode(
            {
                "id": request.user.id,
                "iat": datetime.now(),
                "exp": datetime.now() + timedelta(days=7),
            },
            settings.JWT_SECRET,
            algorithm="HS256"
        )

        return JsonResponse({
            "token": token
        })