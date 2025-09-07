from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Dispatch
from .serializers import DispatchSerializer
from user.models import User
from django.db import models

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.db import models
from django.shortcuts import get_object_or_404

from .models import User, Dispatch
from .serializers import RiderSerializer, DispatchSerializer



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






def get_user_from_token(request):
    """
    Helper function to get the user instance from JWT token in Authorization header.
    """
    token = request.headers.get("Authorization")
    if not token:
        return None, Response({"error": "Authorization token is missing."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token_str = token.split()[1]  # Expecting "Bearer <token>"
        payload = AccessToken(token_str)
        user = get_object_or_404(User, id=payload['user_id'])
        return user, None
    except (IndexError, TokenError, KeyError, User.DoesNotExist):
        return None, Response({"error": "Invalid token or user not found."}, status=status.HTTP_401_UNAUTHORIZED)


class RiderStats(APIView):
    """
    Returns rider statistics like total deliveries, completed jobs, and earnings.
    """
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        if not user.is_rider:
            return Response({"error": "User is not a rider."}, status=status.HTTP_403_FORBIDDEN)

        all_jobs = Dispatch.objects.filter(rider=user)
        completed_jobs = all_jobs.filter(status=Dispatch.Status.DELIVERED).count()
        total_earnings = all_jobs.filter(status=Dispatch.Status.DELIVERED).aggregate(
            total=models.Sum('total_cost')
        )['total'] or 0

        return Response({
            "jobs": all_jobs.count(),
            "completed_jobs": completed_jobs,
            "total_earnings": total_earnings,
        }, status=status.HTTP_200_OK)


class RiderProfile(APIView):
    """
    Returns rider profile details.
    """
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        if not user.is_rider:
            return Response({"error": "User is not a rider."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RiderSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RiderOrders(APIView):
    """
    Returns all orders assigned to the rider, most recent first.
    """
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        if not user.is_rider:
            return Response({"error": "User is not a rider."}, status=status.HTTP_403_FORBIDDEN)

        orders = Dispatch.objects.filter(rider=user).order_by("-created_at")
        serializer = DispatchSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
