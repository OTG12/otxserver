from rest_framework import serializers
from user.models import User
from .models import Dispatch


class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "latitude", "longitude"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class DispatchSerializer(serializers.ModelSerializer):
    rider = RiderSerializer(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Dispatch
        fields = [
            "id",
            "tracking_id",
            "client",
            "rider",
            "package_weight",        # read-only, admin decides
            "package_description",   # user can provide
            "total_cost",            # read-only, admin decides
            "sender_name",
            "sender_email",
            "sender_phone_number",
            "recipient_name",
            "recipient_email",
            "destination_phone_number",
            "pickup_location",       # string
            "destination_location",  # string
            "status",
            "created_at",
            "updated_at",
            "payment_status",        # read-only, admin decides
            "duration",
        ]
        read_only_fields = [
            "id",
            "tracking_id",
            "created_at",
            "updated_at",
            "status",
            "package_weight",
            "total_cost",
            "payment_status",
        ]
