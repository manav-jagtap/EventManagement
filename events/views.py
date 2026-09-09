from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User
from .forms import EventForm
from .models import Category, Event


def organizer_required(view_func):
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
    ).select_related("category", "organizer")

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

    return render(request, "events/event_list.html", {
        "events": events,
        "categories": Category.objects.all(),
        "query": query,
        "selected_category": category,
    })


def event_detail(request, slug):
    event = get_object_or_404(
        Event.objects.select_related("category", "organizer"),
        slug=slug,
    )

    if event.status != Event.Status.PUBLISHED:
        if not request.user.is_authenticated or not (
            request.user.is_superuser
            or event.organizer_id == request.user.pk
        ):
            raise PermissionDenied

    return render(request, "events/event_detail.html", {"event": event})


@organizer_required
def my_events(request):
    events = Event.objects.filter(
        organizer=request.user
    ).select_related("category")

    return render(request, "events/my_events.html", {"events": events})


def generate_unique_slug(title, instance=None):
    base_slug = slugify(title) or "event"
    slug = base_slug
    counter = 2

    while Event.objects.filter(slug=slug).exclude(
        pk=instance.pk if instance else None
    ).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


@organizer_required
def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.slug = generate_unique_slug(event.title)
        event.save()
        messages.success(request, "Event created successfully.")
        return redirect("my_events")

    return render(request, "events/event_form.html", {
        "form": form,
        "page_title": "Create Event",
    })


@organizer_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    form = EventForm(
        request.POST or None,
        request.FILES or None,
        instance=event,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Event updated successfully.")
        return redirect("my_events")

    return render(request, "events/event_form.html", {
        "form": form,
        "page_title": "Edit Event",
        "event": event,
    })


@organizer_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect("my_events")

    return render(request, "events/event_confirm_delete.html", {
        "event": event,
    })