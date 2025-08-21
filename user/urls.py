from . import views
from django.urls import path

urlpatterns = [
    path('create/', views.UserSignUpViews.as_view(), name="User Signup"),
    path('login', views.UserLoginView.as_view(), name="Login Users"),
    path('', views.AllUsers.as_view(), name="All users"),
    path("riders/", views.RiderListView.as_view(), name="rider-list"),
]

#test@yopmail.com

# {
#     "email": "test@yopmail.com",
#     "password": "test@yopmail.com"
# }