import json
from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import User


class RiderTrackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # get rider_id from route if available
        self.rider_id = self.scope["url_route"]["kwargs"].get("rider_id", None)

        # make group name
        if self.rider_id:
            self.group_name = f"rider_{self.rider_id}"
        else:
            self.group_name = "riders"

        # join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        rider_id = data.get("rider_id")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if rider_id:
            # update rider location in DB
            await self.update_rider_location(rider_id, latitude, longitude)

            # broadcast to group of that rider
            await self.channel_layer.group_send(
                f"rider_{rider_id}",
                {
                    "type": "send_location",
                    "rider_id": rider_id,
                    "latitude": latitude,
                    "longitude": longitude,
                },
            )

            # also broadcast to global group (all riders)
            await self.channel_layer.group_send(
                "riders",
                {
                    "type": "send_location",
                    "rider_id": rider_id,
                    "latitude": latitude,
                    "longitude": longitude,
                },
            )

    async def send_location(self, event):
        await self.send(text_data=json.dumps(event))

    @staticmethod
    async def update_rider_location(rider_id, latitude, longitude):
        try:
            rider = User.objects.get(id=rider_id, is_rider=True)
            rider.latitude = latitude
            rider.longitude = longitude
            rider.save()
        except User.DoesNotExist:
            pass
