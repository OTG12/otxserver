from django.urls import path
from .views import (
    PackageListCreateView,
    PackageDetailView,
    PackageSearchView,
    DispatchListCreateView,
    DispatchDetailView,
    DispatchSearchView,
)

urlpatterns = [
    path("packages/", PackageListCreateView.as_view(), name="package-list-create"),
    path("packages/<int:id>/", PackageDetailView.as_view(), name="package-detail"),
    path("packages/search/", PackageSearchView.as_view(), name="package-search"),

    path("", DispatchListCreateView.as_view(), name="dispatch-list-create"),
    path("<int:id>/", DispatchDetailView.as_view(), name="dispatch-detail"),
    path("search/<str:tracking_id>", DispatchSearchView.as_view(), name="dispatch-search"),
]
