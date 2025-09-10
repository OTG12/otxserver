from rest_framework import serializers
from .models import KYC
from user.models import User
from file.models import File

class KYCSerializer(serializers.ModelSerializer):
    # Accept user ID and file IDs on create/update
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    document = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), many=True)
    license_document = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), many=True)

    # Custom read-only fields for GET
    user_email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    document_urls = serializers.SerializerMethodField()
    license_document_urls = serializers.SerializerMethodField()

    class Meta:
        model = KYC
        fields = [
            "id",
            "user",
            "user_email",
            "username",
            "phone_number",
            "fullname",
            "doc_type",
            "document_id",
            "document",
            "document_urls",
            "licence_id",
            "license_document",
            "license_document_urls",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_document_urls(self, obj):
        return [file.url for file in obj.document.all()]

    def get_license_document_urls(self, obj):
        return [file.url for file in obj.license_document.all()]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        
        # Automatically update user.is_rider based on KYC status
        if instance.status == "approved":
            instance.user.is_rider = True
        else:
            instance.user.is_rider = False
        instance.user.save()
        return instance
