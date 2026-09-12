from functools import wraps
from io import BytesIO
from uuid import UUID
import base64

import qrcode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import User
from events.models import Event

from .models import Registration
from .services import book_event, cancel_registration


def attendee_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if (
            not request.user.is_active
            or request.user.role != User.Role.ATTENDEE
        ):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


def organizer_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (
            request.user.is_superuser
            or request.user.role == User.Role.ORGANIZER
        ):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


def get_verify_ticket_url(ticket_code):
    verify_url = reverse("verify_ticket")
    return f"{verify_url}?ticket={ticket_code}"


@attendee_required
@require_POST
def register_event(request, event_id):
    event = get_object_or_404(
        Event,
        pk=event_id,
    )

    try:
        registration = book_event(
            request.user,
            event.pk,
        )

        if registration.status == Registration.Status.CONFIRMED:
            messages.success(
                request,
                "Your seat is confirmed!",
            )
        else:
            messages.info(
                request,
                "Event is full. You have joined the waitlist.",
            )

    except ValidationError as exc:
        messages.error(
            request,
            "; ".join(exc.messages),
        )

    return redirect(
        "event_detail",
        slug=event.slug,
    )


@attendee_required
def my_bookings(request):
    registrations = (
        Registration.objects.filter(
            user=request.user,
        )
        .select_related(
            "event",
            "event__category",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "registrations/my_bookings.html",
        {
            "registrations": registrations,
        },
    )


@attendee_required
def ticket_detail(request, ticket_code):
    registration = get_object_or_404(
        Registration.objects.select_related(
            "event",
            "event__category",
            "event__organizer",
        ),
        ticket_code=ticket_code,
        user=request.user,
        status=Registration.Status.CONFIRMED,
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=3,
    )

    qr.add_data(
        str(registration.ticket_code)
    )
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    buffer = BytesIO()
    image.save(
        buffer,
        format="PNG",
    )

    qr_image = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return render(
        request,
        "registrations/ticket_detail.html",
        {
            "registration": registration,
            "qr_image": qr_image,
        },
    )


@attendee_required
@require_POST
def cancel_booking(request, registration_id):
    registration = get_object_or_404(
        Registration,
        pk=registration_id,
        user=request.user,
    )

    try:
        cancel_registration(
            request.user,
            registration.pk,
        )

        messages.success(
            request,
            "Your registration has been cancelled.",
        )

    except ValidationError as exc:
        messages.error(
            request,
            "; ".join(exc.messages),
        )

    return redirect("my_bookings")


@organizer_required
def verify_ticket(request):
    registration = None
    ticket_code = request.GET.get(
        "ticket",
        "",
    ).strip()

    if ticket_code:
        try:
            ticket_uuid = UUID(ticket_code)

        except ValueError:
            messages.error(
                request,
                "Invalid ticket ID.",
            )

        else:
            registration = (
                Registration.objects
                .select_related(
                    "user",
                    "event",
                )
                .filter(
                    ticket_code=ticket_uuid,
                )
                .first()
            )

            if registration and (
                not request.user.is_superuser
                and registration.event.organizer_id
                != request.user.pk
            ):
                raise PermissionDenied

    return render(
        request,
        "registrations/verify_ticket.html",
        {
            "registration": registration,
            "ticket_code": ticket_code,
        },
    )


@organizer_required
@require_POST
def check_in_ticket(request, registration_id):
    registration = get_object_or_404(
        Registration.objects.select_related(
            "event",
        ),
        pk=registration_id,
    )

    if (
        not request.user.is_superuser
        and registration.event.organizer_id
        != request.user.pk
    ):
        raise PermissionDenied

    verify_url = get_verify_ticket_url(
        registration.ticket_code
    )

    if registration.status != Registration.Status.CONFIRMED:
        messages.error(
            request,
            "Only confirmed registrations can be checked in.",
        )

        return redirect(verify_url)

    if registration.checked_in_at:
        messages.info(
            request,
            "This ticket has already been checked in.",
        )

        return redirect(verify_url)

    registration.checked_in_at = timezone.now()

    registration.save(
        update_fields=["checked_in_at"],
    )

    messages.success(
        request,
        "Attendee checked in successfully.",
    )

    return redirect(verify_url)