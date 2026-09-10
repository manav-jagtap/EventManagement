from django.urls import path

from . import views

urlpatterns = [
    path("my/", views.my_bookings, name="my_bookings"),
    path("tickets/<uuid:ticket_code>/", views.ticket_detail, name="ticket_detail"),
    path("verify/", views.verify_ticket, name="verify_ticket"),
    path("check-in/<int:registration_id>/", views.check_in_ticket, name="check_in_ticket"),
    path("events/<int:event_id>/register/", views.register_event, name="register_event"),
    path("<int:registration_id>/cancel/", views.cancel_booking, name="cancel_booking"),
]