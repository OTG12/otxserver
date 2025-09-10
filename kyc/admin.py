from django.contrib import admin
from .models import KYC


@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = (
        "fullname",
        "user",
        "doc_type",
        "document_id",
        "licence_id",
        "status",
        "created_at",
    )
    list_filter = ("status", "doc_type", "created_at")
    search_fields = ("fullname", "user__username", "document_id", "licence_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("status",)  # allow quick status update
    filter_horizontal = ("document", "license_document")  # for ManyToMany fields

