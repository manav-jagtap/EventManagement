from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User
from events.models import Category, Event


class Command(BaseCommand):
    help = "Create or update 10 realistic EventHub demo events with banners."

    def handle(self, *args, **options):
        try:
            organizer1 = User.objects.get(username="Organizer01")
            organizer2 = User.objects.get(username="Organizer02")

        except User.DoesNotExist as exc:
            raise CommandError(
                "Organizer01 and Organizer02 must exist before running this command."
            ) from exc

        if (
            organizer1.role != User.Role.ORGANIZER
            or organizer2.role != User.Role.ORGANIZER
        ):
            raise CommandError(
                "Organizer01 and Organizer02 must both have organizer role."
            )

        banner_dir = Path(settings.BASE_DIR) / "demo_banners"

        events = [
            {
                "organizer": organizer1,
                "category": "Technology",
                "title": "FutureTech Maharashtra 2026",
                "description": (
                    "A future-focused technology conference featuring AI, "
                    "cloud computing, cybersecurity, developer tools and "
                    "emerging digital trends. Designed for students, "
                    "developers, founders and technology enthusiasts."
                ),
                "venue": "Bal Gandharva Rang Mandir",
                "address": "Jangali Maharaj Road, Shivajinagar",
                "city": "Pune",
                "start_at": "2026-10-10 10:00",
                "end_at": "2026-10-10 17:30",
                "price": 0,
                "seat_limit": 180,
                "banner": "futuretech_maharashtra_2026.png",
            },
            {
                "organizer": organizer1,
                "category": "Workshop",
                "title": "Python & Django Hands-on Bootcamp",
                "description": (
                    "A practical coding workshop covering Python fundamentals, "
                    "Django, models, templates, forms and building a web "
                    "application. Participants are encouraged to bring their own laptop."
                ),
                "venue": "COCSIT Seminar Hall",
                "address": "Ambejogai Road",
                "city": "Latur",
                "start_at": "2026-10-18 09:30",
                "end_at": "2026-10-18 16:30",
                "price": 0,
                "seat_limit": 70,
                "banner": "python_django_bootcamp.png",
            },
            {
                "organizer": organizer2,
                "category": "Music",
                "title": "Mumbai Live Music Night",
                "description": (
                    "An energetic evening of live bands, contemporary music "
                    "and stage performances in Mumbai. A social music experience "
                    "for students, professionals and live-music fans."
                ),
                "venue": "St. Andrew's Auditorium",
                "address": "St Dominic Road, Bandra West",
                "city": "Mumbai",
                "start_at": "2026-10-24 18:30",
                "end_at": "2026-10-24 22:00",
                "price": 0,
                "seat_limit": 250,
                "banner": "mumbai_live_music_night.png",
            },
            {
                "organizer": organizer2,
                "category": "Business",
                "title": "Startup Connect Maharashtra 2026",
                "description": (
                    "A startup and entrepreneurship networking event bringing "
                    "together students, founders, professionals and mentors "
                    "for talks, networking and idea exchange."
                ),
                "venue": "Jio World Convention Centre",
                "address": "Bandra Kurla Complex, Bandra East",
                "city": "Mumbai",
                "start_at": "2026-11-01 10:00",
                "end_at": "2026-11-01 18:00",
                "price": 0,
                "seat_limit": 300,
                "banner": "startup_connect_maharashtra_2026.png",
            },
            {
                "organizer": organizer1,
                "category": "Sports",
                "title": "Latur Weekend Football Cup",
                "description": (
                    "A community football tournament featuring local teams, "
                    "competitive matches and an energetic match-day atmosphere "
                    "for players and football fans."
                ),
                "venue": "District Sports Complex",
                "address": "Latur City",
                "city": "Latur",
                "start_at": "2026-11-08 08:00",
                "end_at": "2026-11-08 18:00",
                "price": 0,
                "seat_limit": 220,
                "banner": "latur_weekend_football_cup.png",
            },
            {
                "organizer": organizer2,
                "category": "Cultural",
                "title": "Pune Art & Culture Fest",
                "description": (
                    "A colourful celebration of art, cultural performances, "
                    "exhibitions, creative installations and local talent "
                    "in a festival-style setting."
                ),
                "venue": "Fergusson College Campus",
                "address": "Fergusson College Road, Shivajinagar",
                "city": "Pune",
                "start_at": "2026-11-15 11:00",
                "end_at": "2026-11-15 21:00",
                "price": 0,
                "seat_limit": 250,
                "banner": "pune_art_culture_fest.png",
            },
            {
                "organizer": organizer1,
                "category": "Food & Entertainment",
                "title": "Nashik Food & Music Carnival",
                "description": (
                    "An evening carnival featuring food stalls, local flavours, "
                    "live music, social spaces and a relaxed festival atmosphere."
                ),
                "venue": "Sula Vineyards Event Lawn",
                "address": "Gangapur-Savargaon Road",
                "city": "Nashik",
                "start_at": "2026-11-22 16:00",
                "end_at": "2026-11-22 22:00",
                "price": 0,
                "seat_limit": 350,
                "banner": "nashik_food_music_carnival.png",
            },
            {
                "organizer": organizer2,
                "category": "Creative",
                "title": "Nagpur Design & Creative Summit",
                "description": (
                    "A creative-industry meetup for designers, creators and "
                    "students with portfolio discussions, visual showcases, "
                    "panel conversations and collaborative sessions."
                ),
                "venue": "Chitnavis Centre",
                "address": "Civil Lines",
                "city": "Nagpur",
                "start_at": "2026-11-29 10:30",
                "end_at": "2026-11-29 17:30",
                "price": 0,
                "seat_limit": 160,
                "banner": "nagpur_design_creative_summit.png",
            },
            {
                "organizer": organizer1,
                "category": "Sports",
                "title": "Kolhapur Marathon & Fitness Expo",
                "description": (
                    "A city fitness event combining a community marathon "
                    "experience with fitness stalls, wellness activities "
                    "and an energetic sports atmosphere."
                ),
                "venue": "Shivaji University Ground",
                "address": "Vidya Nagar",
                "city": "Kolhapur",
                "start_at": "2026-12-06 06:00",
                "end_at": "2026-12-06 12:30",
                "price": 0,
                "seat_limit": 500,
                "banner": "kolhapur_marathon_fitness_expo.png",
            },
            {
                "organizer": organizer2,
                "category": "Photography",
                "title": "Heritage Photography Walk",
                "description": (
                    "A guided photography-focused heritage walk for students, "
                    "travellers and photography enthusiasts, with opportunities "
                    "to capture architecture, landscapes and historic surroundings."
                ),
                "venue": "Bibi Ka Maqbara",
                "address": "Begumpura",
                "city": "Chhatrapati Sambhajinagar",
                "start_at": "2026-12-13 07:00",
                "end_at": "2026-12-13 11:00",
                "price": 0,
                "seat_limit": 80,
                "banner": "heritage_photography_walk.png",
            },
        ]

        created_count = 0
        updated_count = 0

        for item in events:
            category, _ = Category.objects.get_or_create(
                name=item["category"],
                defaults={
                    "slug": slugify(item["category"])
                },
            )

            start_at = timezone.make_aware(
                datetime.strptime(
                    item["start_at"],
                    "%Y-%m-%d %H:%M",
                )
            )

            end_at = timezone.make_aware(
                datetime.strptime(
                    item["end_at"],
                    "%Y-%m-%d %H:%M",
                )
            )

            event, created = Event.objects.update_or_create(
                title=item["title"],
                defaults={
                    "organizer": item["organizer"],
                    "category": category,
                    "slug": slugify(item["title"]),
                    "description": item["description"],
                    "venue": item["venue"],
                    "address": item["address"],
                    "city": item["city"],
                    "start_at": start_at,
                    "end_at": end_at,
                    "price": item["price"],
                    "seat_limit": item["seat_limit"],
                    "status": Event.Status.PUBLISHED,
                },
            )

            banner_path = banner_dir / item["banner"]

            if banner_path.exists():
                with banner_path.open("rb") as image_file:
                    event.banner.save(
                        item["banner"],
                        File(image_file),
                        save=True,
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Banner not found: {banner_path}"
                    )
                )

            if created:
                created_count += 1
                action = "Created"
            else:
                updated_count += 1
                action = "Updated"

            self.stdout.write(
                self.style.SUCCESS(
                    f"{action}: "
                    f"{event.title} "
                    f"-> "
                    f"{event.organizer.username}"
                )
            )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. "
                f"Created {created_count}, "
                f"updated {updated_count} demo events."
            )
        )