from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Package, Dispatch
from .serializers import PackageSerializer, DispatchSerializer


# -----------------------
# PACKAGE VIEWS
# -----------------------

# 1. GENERIC VIEW for Package (list + create)
class PackageListCreateView(generics.ListCreateAPIView):
    queryset = Package.objects.all().order_by("-id")
    serializer_class = PackageSerializer


# 2. GENERIC VIEW for Retrieve, Update, Delete
class PackageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = "id"


# 3. APIView for search by description (or other fields)
class PackageSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q", None)

        if not query:
            return Response(
                {"error": "q query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        packages = Package.objects.filter(
            Q(description__icontains=query) |
            Q(cost__icontains=query) |
            Q(weight__icontains=query)
        ).order_by("-id")

        if not packages.exists():
            return Response(
                {"message": "No package found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -----------------------
# DISPATCH VIEWS (from before)
# -----------------------

class DispatchListCreateView(generics.ListCreateAPIView):
    queryset = Dispatch.objects.all().order_by("-created_at")
    serializer_class = DispatchSerializer


class DispatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    lookup_field = "id"


class DispatchSearchView(APIView):
    def get(self, request, tracking_id):
        dispatches = Dispatch.objects.filter(
            Q(tracking_id__icontains=tracking_id)
        ).order_by("-created_at")

        if not dispatches.exists():
            return Response(
                {"message": "No dispatch found with this tracking ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DispatchSerializer(dispatches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
