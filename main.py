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


class Package(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Package {self.id} - {self.description[:20] if self.description else 'No desc'}"


class Location(models.Model):
    address = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.CharField(max_length=55, null=True, blank=True)
    longitude = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.address or "Unknown location"


class Dispatch(models.Model):
    package = models.ManyToManyField(Package)
    sender_name = models.CharField(max_length=155, null=True, blank=True)
    sender_email = models.EmailField()
    recipient_name = models.CharField(max_length=155, null=True, blank=True)
    sender_phone_number = models.CharField(max_length=20, null=True, blank=True)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="pickup_dispatches")
    destination_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="destination_dispatches")
    destination_phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Dispatch {self.tracking_id} - {self.status}"

    def save(self, *args, **kwargs):
        
        if not self.tracking_id:
            new_id = generate_tracking_id()
            while Dispatch.objects.filter(tracking_id=new_id).exists():
                new_id = generate_tracking_id()
            self.tracking_id = new_id

        self.updated_at = timezone.now()  
        super().save(*args, **kwargs)     
