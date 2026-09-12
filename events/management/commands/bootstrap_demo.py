import os

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from accounts.models import User


class Command(BaseCommand):
    help = "Create demo users and seed EventHub demo events."

    def handle(self, *args, **options):
        admin_password = os.getenv("ADMIN_PASSWORD")
        organizer01_password = os.getenv("ORGANIZER01_PASSWORD")
        organizer02_password = os.getenv("ORGANIZER02_PASSWORD")

        if not all([
            admin_password,
            organizer01_password,
            organizer02_password,
        ]):
            raise CommandError(
                "ADMIN_PASSWORD, ORGANIZER01_PASSWORD and "
                "ORGANIZER02_PASSWORD must be set."
            )

        self.create_user(
            username="EventHubAdmin",
            email="admin@eventhub.local",
            password=admin_password,
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True,
        )

        self.create_user(
            username="Organizer01",
            email="organizer01@eventhub.local",
            password=organizer01_password,
            role=User.Role.ORGANIZER,
        )

        self.create_user(
            username="Organizer02",
            email="organizer02@eventhub.local",
            password=organizer02_password,
            role=User.Role.ORGANIZER,
        )

        call_command("seed_demo_events")

        self.stdout.write(
            self.style.SUCCESS("EventHub demo setup completed.")
        )

    def create_user(
        self,
        username,
        email,
        password,
        role,
        is_staff=False,
        is_superuser=False,
    ):
        user, _ = User.objects.get_or_create(username=username)

        user.email = email
        user.role = role
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = True
        user.set_password(password)
        user.save()

        self.stdout.write(f"Ready: {username}")