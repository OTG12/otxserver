from rest_framework import generics, permissions
from .models import KYC
from .serializers import KYCSerializer
from user.permissions import IsAdminOrStaff


class KYCListCreateView(generics.ListCreateAPIView):
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return KYC.objects.all().select_related('user').prefetch_related('document', 'license_document')
        return KYC.objects.filter(user=user).select_related('user').prefetch_related('document', 'license_document')


class KYCDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = KYCSerializer
    permission_classes = [IsAdminOrStaff]
    queryset = KYC.objects.all().select_related('user').prefetch_related('document', 'license_document')
