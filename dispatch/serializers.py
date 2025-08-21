from rest_framework import serializers
from .models import Package, Location, Dispatch


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ["id", "description", "weight", "cost"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "address", "latitude", "longitude"]


class DispatchSerializer(serializers.ModelSerializer):
    package = PackageSerializer(many=True, read_only=True)  # nested view
    package_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Package.objects.all(), write_only=True, source="package"
    )
    pickup_location = LocationSerializer(read_only=True)
    destination_location = LocationSerializer(read_only=True)
    pickup_location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), write_only=True, source="pickup_location"
    )
    destination_location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), write_only=True, source="destination_location"
    )

    class Meta:
        model = Dispatch
        fields = [
            "id",
            "tracking_id",
            "client",
            "rider",
            "package",
            "package_ids",
            "total_cost",
            "sender_name",
            "sender_email",
            "recipient_name",
            "sender_phone_number",
            "pickup_location",
            "pickup_location_id",
            "destination_location",
            "destination_location_id",
            "destination_phone_number",
            "status",
            "created_at",
            "updated_at",
            "payment_status",
            "duration",
        ]
        read_only_fields = ["id", "tracking_id", "created_at", "updated_at"]

