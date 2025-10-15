from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .auth_views import RegisterView, LoginView
from .views import (
    TeamListCreateView, BookRoomView, CancelBookingView,
    AllBookedRoomsView, AvailableRoomsView
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),

    path("teams/", TeamListCreateView.as_view()),
    path("book/", BookRoomView.as_view()),
    path("cancel/<int:pk>/", CancelBookingView.as_view()),
    path("booked/", AllBookedRoomsView.as_view()),
    path("available/", AvailableRoomsView.as_view()),
]
