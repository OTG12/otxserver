import uuid
import random
import string
from django.utils import timezone
from django.db import models
from user.models import User


def generate_tracking_id():
    """Generate a random tracking ID like TRK-ABC12345"""
    prefix = "TRK"
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{random_str}"

class Dispatch(models.Model):
    class Status(models.TextChoices):
        PACKING = "PACKING", "Packing"
        EN_ROUTE = "EN_ROUTE", "En Route"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_id = models.CharField(max_length=30, unique=True, editable=False, blank=True)
    client = models.ForeignKey(User, related_name="client_dispatches", on_delete=models.SET_NULL, null=True, blank=True)
    rider = models.ForeignKey(User, related_name="rider_dispatches", on_delete=models.SET_NULL, null=True, blank=True)

    package_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_description = models.TextField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    sender_name = models.CharField(max_length=155, null=True, blank=True)
    sender_email = models.EmailField()
    sender_phone_number = models.CharField(max_length=20, null=True, blank=True)

    recipient_name = models.CharField(max_length=155, null=True, blank=True)
    recipient_email = models.EmailField(null=True, blank=True)   # ✅ Added
    destination_phone_number = models.CharField(max_length=20)

    pickup_location = models.CharField(max_length=500, null=True, blank=True)
    destination_location = models.CharField(max_length=500, null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PACKING)
    payment_status = models.BooleanField(default=False)
    duration = models.DurationField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispatch {self.tracking_id} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            new_id = generate_tracking_id()
            while Dispatch.objects.filter(tracking_id=new_id).exists():
                new_id = generate_tracking_id()
            self.tracking_id = new_id
        super().save(*args, **kwargs)
