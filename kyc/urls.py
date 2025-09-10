from django.urls import path
from .views import KYCListCreateView, KYCDetailView

urlpatterns = [
    path("", KYCListCreateView.as_view(), name="kyc-list-create"),
    path("<uuid:id>/", KYCDetailView.as_view(), name="kyc-detail"),
]
