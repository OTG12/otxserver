from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import KYC
from .serializers import KYCSerializer
from user.permissions import IsAdminOrStaff


class KYCListCreateView(generics.ListCreateAPIView):
    queryset = KYC.objects.all().order_by("-created_at")
    serializer_class = KYCSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        kyc = serializer.save()
        # update user.is_rider based on status
        if kyc.status == "approved":
            kyc.user.is_rider = True
        else:
            kyc.user.is_rider = False
        kyc.user.save()


class KYCDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer
    lookup_field = "id"
    permission_classes = [IsAdminOrStaff]

    def perform_update(self, serializer):
        kyc = serializer.save()
        if kyc.status == "approved":
            kyc.user.is_rider = True
        else:
            kyc.user.is_rider = False
        kyc.user.save()
