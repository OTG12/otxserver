from django.urls import path
from .views import (
    DispatchListCreateView,
    DispatchDetailView,
    DispatchSearchView,
    RiderStats,
    RiderProfile,
    RiderOrders
)

urlpatterns = [
    path("", DispatchListCreateView.as_view(), name="dispatch-list-create"),
    path("<int:id>/", DispatchDetailView.as_view(), name="dispatch-detail"),
    path("search/<str:tracking_id>", DispatchSearchView.as_view(), name="dispatch-search"),
    path("riders/stats", RiderStats.as_view(), name="rider-stats"),
    path("riders/profile", RiderProfile.as_view(), name="rider-profile"),
    path("riders/orders", RiderOrders.as_view(), name="rider-orders"),
]
