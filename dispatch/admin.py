from django.contrib import admin
from .models import Package, Location, Dispatch


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "weight", "cost")
    search_fields = ("description",)
    ordering = ("-id",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "address", "latitude", "longitude")
    search_fields = ("address",)


@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = (
        "tracking_id",
        "client",
        "rider",
        "status",
        "total_cost",
        "payment_status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "payment_status", "created_at")
    search_fields = ("tracking_id", "sender_name", "recipient_name", "sender_email")
    ordering = ("-created_at",)
    readonly_fields = ("tracking_id", "created_at", "updated_at")  # auto fields
    filter_horizontal = ("package",)  # nicer UI for many-to-many packages
