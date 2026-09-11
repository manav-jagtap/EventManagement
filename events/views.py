from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User
from .forms import EventForm
from .models import Category, Event


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


def event_list(request):
    events = Event.objects.filter(
        status=Event.Status.PUBLISHED,
        start_at__gte=timezone.now(),
    ).select_related(
        "category",
        "organizer",
    )

    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    if query:
        events = events.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(city__icontains=query)
        )

    if category:
        events = events.filter(category__slug=category)

    return render(
        request,
        "events/event_list.html",
        {
            "events": events,
            "categories": Category.objects.all(),
            "query": query,
            "selected_category": category,
        },
    )


def event_detail(request, slug):
    event = get_object_or_404(
        Event.objects.select_related(
            "category",
            "organizer",
        ),
        slug=slug,
    )

    if event.status != Event.Status.PUBLISHED:
        if not request.user.is_authenticated or not (
            request.user.is_superuser
            or event.organizer_id == request.user.pk
        ):
            raise PermissionDenied

    confirmed_count = event.registrations.filter(
        status="confirmed"
    ).count()

    available_seats = max(
        event.seat_limit - confirmed_count,
        0,
    )

    user_registration = None

    if request.user.is_authenticated:
        user_registration = event.registrations.filter(
            user=request.user,
            status__in=[
                "confirmed",
                "waitlisted",
            ],
        ).first()

    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,
            "available_seats": available_seats,
            "user_registration": user_registration,
        },
    )


@organizer_required
def my_events(request):
    events = Event.objects.filter(
        organizer=request.user
    ).select_related("category")

    return render(
        request,
        "events/my_events.html",
        {
            "events": events,
        },
    )


@organizer_required
def organizer_analytics(request):
    events = (
        Event.objects.filter(
            organizer=request.user
        )
        .annotate(
            total_registrations=Count(
                "registrations",
            ),
            confirmed_registrations=Count(
                "registrations",
                filter=Q(
                    registrations__status="confirmed"
                ),
            ),
            waitlisted_registrations=Count(
                "registrations",
                filter=Q(
                    registrations__status="waitlisted"
                ),
            ),
            checked_in_registrations=Count(
                "registrations",
                filter=Q(
                    registrations__checked_in_at__isnull=False
                ),
            ),
        )
        .select_related("category")
        .order_by("-start_at")
    )

    total_events = events.count()

    total_registrations = sum(
        event.total_registrations
        for event in events
    )

    confirmed_count = sum(
        event.confirmed_registrations
        for event in events
    )

    waitlisted_count = sum(
        event.waitlisted_registrations
        for event in events
    )

    checked_in_count = sum(
        event.checked_in_registrations
        for event in events
    )

    attendance_rate = (
        round(
            (checked_in_count / confirmed_count) * 100,
            1,
        )
        if confirmed_count
        else 0
    )

    for event in events:
        event.attendance_rate = (
            round(
                (
                    event.checked_in_registrations
                    / event.confirmed_registrations
                )
                * 100,
                1,
            )
            if event.confirmed_registrations
            else 0
        )

    return render(
        request,
        "events/organizer_analytics.html",
        {
            "events": events,
            "total_events": total_events,
            "total_registrations": total_registrations,
            "confirmed_count": confirmed_count,
            "waitlisted_count": waitlisted_count,
            "checked_in_count": checked_in_count,
            "attendance_rate": attendance_rate,
        },
    )


def generate_unique_slug(title, instance=None):
    base_slug = slugify(title) or "event"
    slug = base_slug
    counter = 2

    while Event.objects.filter(
        slug=slug
    ).exclude(
        pk=instance.pk if instance else None
    ).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


@organizer_required
def event_create(request):
    form = EventForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST" and form.is_valid():
        event = form.save(commit=False)

        event.organizer = request.user
        event.slug = generate_unique_slug(
            event.title
        )

        event.save()

        messages.success(
            request,
            "Event created successfully.",
        )

        return redirect("my_events")

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "page_title": "Create Event",
        },
    )


@organizer_required
def event_update(request, pk):
    if request.method == "POST":
        with transaction.atomic():
            event = get_object_or_404(
                Event.objects.select_for_update(),
                pk=pk,
                organizer=request.user,
            )

            form = EventForm(
                request.POST,
                request.FILES,
                instance=event,
            )

            if form.is_valid():
                form.save()

                messages.success(
                    request,
                    "Event updated successfully.",
                )

                return redirect("my_events")

    else:
        event = get_object_or_404(
            Event,
            pk=pk,
            organizer=request.user,
        )

        form = EventForm(
            instance=event
        )

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "page_title": "Edit Event",
            "event": event,
        },
    )


@organizer_required
def event_delete(request, pk):
    event = get_object_or_404(
        Event,
        pk=pk,
        organizer=request.user,
    )

    if request.method == "POST":
        if event.registrations.exists():
            messages.error(
                request,
                "This event has registrations and cannot be deleted. "
                "Change its status to Cancelled instead.",
            )

            return redirect("my_events")

        event.delete()

        messages.success(
            request,
            "Event deleted successfully.",
        )

        return redirect("my_events")

    return render(
        request,
        "events/event_confirm_delete.html",
        {
            "event": event,
        },
    )