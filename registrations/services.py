from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from events.models import Event
from .models import Registration


def lock_event(event_id):
    """Obtain a SQLite write lock before checking event capacity."""
    Event.objects.filter(pk=event_id).update(
        updated_at=timezone.now()
    )
    return Event.objects.get(pk=event_id)


def confirmed_count(event):
    return Registration.objects.filter(
        event=event,
        status=Registration.Status.CONFIRMED,
    ).count()


@transaction.atomic
def book_event(user, event_id):
    if (
        not user.is_authenticated
        or not user.is_active
        or user.role != User.Role.ATTENDEE
    ):
        raise ValidationError("Only active attendees can register.")

    event = lock_event(event_id)

    if (
        event.status != Event.Status.PUBLISHED
        or event.start_at <= timezone.now()
    ):
        raise ValidationError("Registration is closed for this event.")

    if event.price > 0:
        raise ValidationError("Paid event registration is not available yet.")

    if Registration.objects.filter(
        user=user,
        event=event,
        status__in=[
            Registration.Status.CONFIRMED,
            Registration.Status.WAITLISTED,
        ],
    ).exists():
        raise ValidationError("You are already registered for this event.")

    has_waitlist = Registration.objects.filter(
        event=event,
        status=Registration.Status.WAITLISTED,
    ).exists()

    status = (
        Registration.Status.CONFIRMED
        if confirmed_count(event) < event.seat_limit and not has_waitlist
        else Registration.Status.WAITLISTED
    )

    return Registration.objects.create(
        user=user,
        event=event,
        status=status,
    )


@transaction.atomic
def cancel_registration(user, registration_id):
    registration = Registration.objects.get(
        pk=registration_id,
        user=user,
    )

    event = lock_event(registration.event_id)
    registration.refresh_from_db()

    if registration.status == Registration.Status.CANCELLED:
        raise ValidationError("This registration is already cancelled.")

    if registration.checked_in_at:
        raise ValidationError("Checked-in tickets cannot be cancelled.")

    if event.start_at <= timezone.now():
        raise ValidationError("Cancellation is closed for this event.")

    was_confirmed = registration.status == Registration.Status.CONFIRMED

    registration.status = Registration.Status.CANCELLED
    registration.save(update_fields=["status"])

    if was_confirmed and event.status == Event.Status.PUBLISHED:
        next_person = (
            Registration.objects.filter(
                event=event,
                status=Registration.Status.WAITLISTED,
            )
            .order_by("created_at", "pk")
            .first()
        )

        if next_person:
            next_person.status = Registration.Status.CONFIRMED
            next_person.save(update_fields=["status"])

    return registration
