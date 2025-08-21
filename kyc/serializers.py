from rest_framework import serializers
from .models import KYC
from user.models import User


class UserBasicSerializer(serializers.ModelSerializer):
    """Minimal user serializer to display basic info in KYC response"""

    class Meta:
        model = User
        fields = ["id", "username", "email"]


class KYCSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)   # nested read-only view
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="user"
    )

    class Meta:
        model = KYC
        fields = [
            "id",
            "user",
            "user_id",
            "doc_type",
            "document_id",
            "document",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def validate_document_id(self, value):
        """Extra validation to prevent duplicate IDs"""
        if KYC.objects.filter(document_id=value).exists():
            raise serializers.ValidationError("This document ID is already registered.")
        return value

    def create(self, validated_data):
        """Ensure KYC starts with pending status always"""
        validated_data["status"] = "pending"
        return super().create(validated_data)
