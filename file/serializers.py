from rest_framework import serializers
from .models import File
from libs.cloudinary import MediaService
from utilities.sanitize import detect_type, scan_pdf_for_malware_bytes


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=True)

    class Meta:
        model = File
        fields = [
            "id",
            "name",
            "slug",
            "url",
            "file_type",
            "size",
            "content_type",
            "description",
            "created_at",
            "updated_at",
            "file",  # upload only
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "slug": {"read_only": True},
            "name": {"read_only": True},
            "url": {"read_only": True},
            "file_type": {"read_only": True},
            "size": {"read_only": True},
            "content_type": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        uploaded_file = validated_data.pop("file")

        # Read file bytes
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)

        # Detect file type
        file_type = detect_type(file_bytes[:1024], file_bytes)
        if not file_type:
            raise serializers.ValidationError("Unsupported or unrecognized file type")

        # Scan PDF if needed
        if file_type == "pdf":
            scan_result = scan_pdf_for_malware_bytes(file_bytes)
            if scan_result is not True:
                raise serializers.ValidationError(scan_result)

        # Upload to Cloudinary
        url = MediaService.upload(uploaded_file)
        if not url:
            raise serializers.ValidationError("Failed to upload file")

        # Create and return the File instance
        return File.objects.create(
            name=uploaded_file.name,  # extracted automatically
            url=url,
            file_type=file_type,
            size=uploaded_file.size,
            content_type=uploaded_file.content_type,
            description=validated_data.get("description", ""),
        )
