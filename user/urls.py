from .views import UserSignUpViews, UserLoginView, AllUsers, RiderListView, UpdateRiderView
from django.urls import path

urlpatterns = [
    path('create/', UserSignUpViews.as_view(), name="User Signup"),
    path('login', UserLoginView.as_view(), name="Login Users"),
    path('', AllUsers.as_view(), name="All users"),
    path("riders/", RiderListView.as_view(), name="rider-list"),
    path("<uuid:id>/", UpdateRiderView.as_view(), name="update-rider"),
]

#test@yopmail.com

# {
#     "email": "test@yopmail.com",
#     "password": "test@yopmail.com"
# }