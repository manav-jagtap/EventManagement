from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


DEMO_BANNER_PATHS = {
    "futuretech-maharashtra-2026":
        "demo_banners/futuretech_maharashtra_2026.png",

    "python-django-hands-on-bootcamp":
        "demo_banners/python_django_bootcamp.png",

    "mumbai-live-music-night":
        "demo_banners/mumbai_live_music_night.png",

    "startup-connect-maharashtra-2026":
        "demo_banners/startup_connect_maharashtra_2026.png",

    "latur-weekend-football-cup":
        "demo_banners/latur_weekend_football_cup.png",

    "pune-art-culture-fest":
        "demo_banners/pune_art_culture_fest.png",

    "nashik-food-music-carnival":
        "demo_banners/nashik_food_music_carnival.png",

    "nagpur-modern-art-exhibition":
        "demo_banners/nagpur_modern_art_exhibition.png",

    "heritage-photography-walk":
        "demo_banners/heritage_photography_walk.png",

    "maharashtra-stand-up-comedy-night":
        "demo_banners/maharashtra_standup_comedy_night.png",

    "latur-kids-carnival-2026":
        "demo_banners/latur_kids_carnival_2026.png",

    "maharashtra-college-esports-championship":
        "demo_banners/maharashtra_college_esports_championship.png",

    "morning-yoga-wellness-experience":
        "demo_banners/morning_yoga_wellness_experience.png",

    "career-higher-education-expo-2027":
        "demo_banners/career_higher_education_expo_2027.png",

    "latur-youth-community-meetup":
        "demo_banners/latur_youth_community_meetup.png",

    "cocsit-tech-career-connect-2027":
        "demo_banners/cocsit_latur_campus.png",
}


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CANCELLED = "cancelled", "Cancelled"

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="organized_events",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="events",
    )

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
    )

    description = models.TextField()

    banner = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True,
    )

    venue = models.CharField(
        max_length=255,
    )

    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
    )

    start_at = models.DateTimeField()

    end_at = models.DateTimeField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    seat_limit = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["start_at"]

        indexes = [
            models.Index(
                fields=["status", "start_at"],
            ),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        errors = {}

        if (
            self.start_at
            and self.end_at
            and self.end_at <= self.start_at
        ):
            errors["end_at"] = (
                "End date and time must be after the start."
            )

        if (
            self.start_at
            and not self.pk
            and self.start_at <= timezone.now()
        ):
            errors["start_at"] = (
                "A new event must start in the future."
            )

        if self.pk and self.seat_limit is not None:
            confirmed_count = self.registrations.filter(
                status="confirmed",
            ).count()

            if self.seat_limit < confirmed_count:
                errors["seat_limit"] = (
                    f"Seat limit cannot be less than "
                    f"{confirmed_count} confirmed bookings."
                )

        if errors:
            raise ValidationError(errors)

    @property
    def is_free(self):
        return self.price == 0

    @property
    def demo_banner_path(self):
        return DEMO_BANNER_PATHS.get(self.slug, "")