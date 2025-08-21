from django.urls import path
from .views import KYCListCreateView, KYCDetailView

urlpatterns = [
    path("kyc/", KYCListCreateView.as_view(), name="kyc-list-create"),
    path("kyc/<uuid:id>/", KYCDetailView.as_view(), name="kyc-detail"),
]
