import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from user.models import User

class RiderTrackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.is_running = True
        asyncio.create_task(self.send_riders_loop())

    async def disconnect(self, close_code):
        self.is_running = False

    async def send_riders_loop(self):
        while self.is_running:
            riders = await self.get_all_riders()
            await self.send(text_data=json.dumps(riders))
            await asyncio.sleep(5)  # update every 5 seconds

    @database_sync_to_async
    def get_all_riders(self):
        return list(User.objects.filter(is_rider=True).values("email", "latitude", "longitude"))
