from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User
from events.models import Category, Event


EVENTS = [
    {
        "organizer": "Organizer01",
        "category": "Technology",
        "title": "FutureTech Maharashtra 2026",
        "description": "A future-focused technology conference featuring artificial intelligence, cloud computing, cybersecurity, developer tools and emerging digital technologies. Designed for students, developers and technology enthusiasts.",
        "venue": "Bal Gandharva Rang Mandir",
        "address": "Jangali Maharaj Road, Shivajinagar",
        "city": "Pune",
        "start_at": "2026-10-10 10:00",
        "end_at": "2026-10-10 17:30",
        "seat_limit": 180,
    },
    {
        "organizer": "Organizer01",
        "category": "Workshop",
        "title": "Python & Django Hands-on Bootcamp",
        "description": "A practical coding workshop covering Python fundamentals, Django models, templates, forms and building a small web application. Participants are encouraged to bring their laptop.",
        "venue": "COCSIT Seminar Hall",
        "address": "Ambejogai Road",
        "city": "Latur",
        "start_at": "2026-10-18 09:30",
        "end_at": "2026-10-18 16:30",
        "seat_limit": 70,
    },
    {
        "organizer": "Organizer02",
        "category": "Music",
        "title": "Mumbai Live Music Night",
        "description": "An energetic evening of live bands, contemporary music and stage performances for students, young professionals and live-music fans.",
        "venue": "St. Andrew's Auditorium",
        "address": "St Dominic Road, Bandra West",
        "city": "Mumbai",
        "start_at": "2026-10-24 18:30",
        "end_at": "2026-10-24 22:00",
        "seat_limit": 250,
    },
    {
        "organizer": "Organizer02",
        "category": "Business",
        "title": "Startup Connect Maharashtra 2026",
        "description": "A startup and entrepreneurship networking event bringing together students, founders, professionals and mentors for talks, networking and idea exchange.",
        "venue": "Jio World Convention Centre",
        "address": "Bandra Kurla Complex, Bandra East",
        "city": "Mumbai",
        "start_at": "2026-11-01 10:00",
        "end_at": "2026-11-01 18:00",
        "seat_limit": 300,
    },
    {
        "organizer": "Organizer01",
        "category": "Sports",
        "title": "Latur Weekend Football Cup",
        "description": "A community football tournament featuring local teams, competitive matches and an energetic match-day atmosphere for players and football fans.",
        "venue": "District Sports Complex",
        "address": "Latur City",
        "city": "Latur",
        "start_at": "2026-11-08 08:00",
        "end_at": "2026-11-08 18:00",
        "seat_limit": 220,
    },
    {
        "organizer": "Organizer02",
        "category": "Arts & Culture",
        "title": "Pune Art & Culture Fest",
        "description": "A colourful celebration of art, cultural performances, creative installations, exhibitions and talented local artists.",
        "venue": "Fergusson College Campus",
        "address": "Fergusson College Road, Shivajinagar",
        "city": "Pune",
        "start_at": "2026-11-15 11:00",
        "end_at": "2026-11-15 21:00",
        "seat_limit": 250,
    },
    {
        "organizer": "Organizer01",
        "category": "Food & Entertainment",
        "title": "Nashik Food & Music Carnival",
        "description": "A lively carnival featuring food stalls, local flavours, live music, entertainment areas and a relaxed social atmosphere.",
        "venue": "Sula Vineyards Event Lawn",
        "address": "Gangapur-Savargaon Road",
        "city": "Nashik",
        "start_at": "2026-11-22 16:00",
        "end_at": "2026-11-22 22:00",
        "seat_limit": 350,
    },
    {
        "organizer": "Organizer02",
        "category": "Exhibition",
        "title": "Nagpur Modern Art Exhibition",
        "description": "A modern exhibition featuring creative artwork, visual installations, student creations and innovative design showcases.",
        "venue": "Chitnavis Centre",
        "address": "Civil Lines",
        "city": "Nagpur",
        "start_at": "2026-11-29 10:30",
        "end_at": "2026-11-29 18:00",
        "seat_limit": 160,
    },
    {
        "organizer": "Organizer02",
        "category": "Photography",
        "title": "Heritage Photography Walk",
        "description": "A guided photography-focused heritage walk for students, travellers and photography enthusiasts with opportunities to capture architecture and historic surroundings.",
        "venue": "Bibi Ka Maqbara",
        "address": "Begumpura",
        "city": "Chhatrapati Sambhajinagar",
        "start_at": "2026-12-13 07:00",
        "end_at": "2026-12-13 11:00",
        "seat_limit": 80,
    },
    {
        "organizer": "Organizer02",
        "category": "Comedy",
        "title": "Maharashtra Stand-up Comedy Night",
        "description": "A fun live comedy evening featuring emerging stand-up comedians, observational humour and audience interaction.",
        "venue": "Yashwantrao Chavan Natyagruha",
        "address": "Kothrud",
        "city": "Pune",
        "start_at": "2026-12-19 19:00",
        "end_at": "2026-12-19 21:30",
        "seat_limit": 220,
    },
    {
        "organizer": "Organizer01",
        "category": "Kids & Family",
        "title": "Latur Kids Carnival 2026",
        "description": "A family-friendly carnival with games, drawing activities, creative workshops, fun competitions and entertainment for children and parents.",
        "venue": "Dayanand College Ground",
        "address": "Barshi Road",
        "city": "Latur",
        "start_at": "2026-12-20 10:00",
        "end_at": "2026-12-20 18:00",
        "seat_limit": 300,
    },
    {
        "organizer": "Organizer01",
        "category": "Gaming",
        "title": "Maharashtra College Esports Championship",
        "description": "A competitive college esports event featuring gaming tournaments, team battles, live matches and gaming zones.",
        "venue": "MIT-WPU Auditorium",
        "address": "Kothrud",
        "city": "Pune",
        "start_at": "2026-12-27 10:00",
        "end_at": "2026-12-27 19:00",
        "seat_limit": 240,
    },
    {
        "organizer": "Organizer02",
        "category": "Health & Wellness",
        "title": "Morning Yoga & Wellness Experience",
        "description": "A refreshing morning wellness event featuring guided yoga, mindfulness, breathing exercises and beginner-friendly wellness sessions.",
        "venue": "Joggers Park",
        "address": "Bandra West",
        "city": "Mumbai",
        "start_at": "2027-01-03 06:30",
        "end_at": "2027-01-03 10:00",
        "seat_limit": 150,
    },
    {
        "organizer": "Organizer01",
        "category": "Education",
        "title": "Career & Higher Education Expo 2027",
        "description": "An education-focused expo for students exploring higher education, career paths, professional certifications and industry opportunities.",
        "venue": "Convention Hall",
        "address": "College Road",
        "city": "Nashik",
        "start_at": "2027-01-10 10:00",
        "end_at": "2027-01-10 17:00",
        "seat_limit": 300,
    },
    {
        "organizer": "Organizer02",
        "category": "Community",
        "title": "Latur Youth Community Meetup",
        "description": "A community meetup where students and young professionals can connect, share ideas, discover opportunities and build strong local networks.",
        "venue": "Town Hall",
        "address": "Central Latur",
        "city": "Latur",
        "start_at": "2027-01-17 16:00",
        "end_at": "2027-01-17 19:30",
        "seat_limit": 120,
    },
    {
        "organizer": "Organizer01",
        "category": "Technology",
        "title": "COCSIT Tech & Career Connect 2027",
        "description": "A special technology and career event for COCSIT students featuring cloud and software career guidance, technical sessions, project showcases and industry discussions.",
        "venue": "COCSIT Campus",
        "address": "Ambejogai Road",
        "city": "Latur",
        "start_at": "2027-01-24 10:00",
        "end_at": "2027-01-24 17:00",
        "seat_limit": 250,
    },
]


def make_datetime(value):
    return timezone.make_aware(
        datetime.fromisoformat(value)
    )


class Command(BaseCommand):
    help = "Create or update the 16 EventHub demo events."

    def handle(self, *args, **options):
        try:
            organizer1 = User.objects.get(
                username="Organizer01"
            )
            organizer2 = User.objects.get(
                username="Organizer02"
            )
        except User.DoesNotExist as exc:
            raise CommandError(
                "Organizer01 and Organizer02 must exist."
            ) from exc

        organizers = {
            "Organizer01": organizer1,
            "Organizer02": organizer2,
        }

        if any(
            user.role != User.Role.ORGANIZER
            for user in organizers.values()
        ):
            raise CommandError(
                "Both demo users must have organizer role."
            )

        category_names = {
            item["category"]
            for item in EVENTS
        }

        categories = {}

        for name in category_names:
            category, _ = Category.objects.update_or_create(
                name=name,
                defaults={
                    "slug": slugify(name),
                },
            )
            categories[name] = category

        created_count = 0
        updated_count = 0

        for item in EVENTS:
            _, created = Event.objects.update_or_create(
                title=item["title"],
                defaults={
                    "organizer": organizers[item["organizer"]],
                    "category": categories[item["category"]],
                    "slug": slugify(item["title"]),
                    "description": item["description"],
                    "venue": item["venue"],
                    "address": item["address"],
                    "city": item["city"],
                    "start_at": make_datetime(item["start_at"]),
                    "end_at": make_datetime(item["end_at"]),
                    "price": 0,
                    "seat_limit": item["seat_limit"],
                    "status": Event.Status.PUBLISHED,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        Category.objects.filter(
            name__in=["Cultural", "Creative"],
            events__isnull=True,
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo seed complete: "
                f"{created_count} created, "
                f"{updated_count} updated, "
                f"{len(EVENTS)} total."
            )
        )