from django.urls import path

from . import views

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("my/", views.my_events, name="my_events"),
    path("create/", views.event_create, name="event_create"),
    path("<slug:slug>/", views.event_detail, name="event_detail"),
    path("<int:pk>/edit/", views.event_update, name="event_update"),
    path("<int:pk>/delete/", views.event_delete, name="event_delete"),
]