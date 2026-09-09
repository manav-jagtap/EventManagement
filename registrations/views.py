from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import User
from events.models import Event
from .models import Registration
from .services import book_event, cancel_registration


def attendee_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if (
            not request.user.is_active
            or request.user.role != User.Role.ATTENDEE
        ):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper


@attendee_required
@require_POST
def register_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    try:
        registration = book_event(request.user, event.pk)
        if registration.status == Registration.Status.CONFIRMED:
            messages.success(request, "Your seat is confirmed!")
        else:
            messages.info(request, "Event is full. You have joined the waitlist.")
    except ValidationError as exc:
        messages.error(request, "; ".join(exc.messages))

    return redirect("event_detail", slug=event.slug)


@attendee_required
def my_bookings(request):
    registrations = (
        Registration.objects.filter(user=request.user)
        .select_related("event", "event__category")
        .order_by("-created_at")
    )

    return render(request, "registrations/my_bookings.html", {
        "registrations": registrations,
    })


@attendee_required
@require_POST
def cancel_booking(request, registration_id):
    registration = get_object_or_404(
        Registration,
        pk=registration_id,
        user=request.user,
    )

    try:
        cancel_registration(request.user, registration.pk)
        messages.success(request, "Your registration has been cancelled.")
    except ValidationError as exc:
        messages.error(request, "; ".join(exc.messages))

    return redirect("my_bookings")