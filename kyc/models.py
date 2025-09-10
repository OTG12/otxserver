import uuid
from django.db import models
from django.utils import timezone
from user.models import User  
from file.models import File


def upload_kyc_document(instance, filename):
    """Store KYC documents under media/kyc/<user_id>/<filename>"""
    return f"kyc/{instance.user.id}/{filename}"


class KYC(models.Model):
    DOC_TYPES = (
        ("nin", "NIN"),
        ("passport", "Passport"),
        ("voter_id", "Voter's ID"),
    )
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="kyc_records")
    fullname = models.CharField(max_length=225, unique=True)
    doc_type = models.CharField(max_length=50, choices=DOC_TYPES)
    document_id = models.CharField(max_length=100)  
    document = models.ManyToManyField(File, related_name="kyc_documents")
    licence_id = models.CharField(max_length=100)  
    license_document = models.ManyToManyField(File, related_name="kyc_license_documents")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "KYC"
        verbose_name_plural = "KYC Records"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "document_id"], name="unique_doc_per_user"),
            models.UniqueConstraint(fields=["user", "licence_id"], name="unique_licence_per_user"),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.doc_type} ({self.status})"
