from django.urls import path
from . import views

urlpatterns = [
    path("reservations/get_reservations", views.ReservationList.as_view(), name="listReservation"),
]