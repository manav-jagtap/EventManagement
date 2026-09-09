from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from events.models import Category, Event
from .models import Registration
from .services import book_event, cancel_registration


class BookingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organizer = User.objects.create_user(
            username="organizer",
            email="organizer@test.com",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )
        cls.attendee1 = User.objects.create_user(
            username="attendee1",
            email="attendee1@test.com",
            password="TestPass123!",
        )
        cls.attendee2 = User.objects.create_user(
            username="attendee2",
            email="attendee2@test.com",
            password="TestPass123!",
        )
        cls.attendee3 = User.objects.create_user(
            username="attendee3",
            email="attendee3@test.com",
            password="TestPass123!",
        )

        cls.category = Category.objects.create(
            name="Technology",
            slug="technology",
        )

        cls.event = Event.objects.create(
            organizer=cls.organizer,
            category=cls.category,
            title="Python Workshop",
            slug="python-workshop",
            description="Test event",
            venue="Seminar Hall",
            city="Latur",
            start_at=timezone.now() + timedelta(days=7),
            end_at=timezone.now() + timedelta(days=7, hours=2),
            price=0,
            seat_limit=1,
            status=Event.Status.PUBLISHED,
        )

    def test_first_booking_is_confirmed(self):
        registration = book_event(self.attendee1, self.event.pk)

        self.assertEqual(
            registration.status,
            Registration.Status.CONFIRMED,
        )

    def test_full_event_creates_waitlist(self):
        book_event(self.attendee1, self.event.pk)
        second = book_event(self.attendee2, self.event.pk)

        self.assertEqual(
            second.status,
            Registration.Status.WAITLISTED,
        )
        self.assertEqual(
            Registration.objects.filter(
                event=self.event,
                status=Registration.Status.CONFIRMED,
            ).count(),
            1,
        )

    def test_duplicate_active_booking_is_rejected(self):
        book_event(self.attendee1, self.event.pk)

        with self.assertRaises(ValidationError):
            book_event(self.attendee1, self.event.pk)

    def test_organizer_cannot_book(self):
        with self.assertRaises(ValidationError):
            book_event(self.organizer, self.event.pk)

    def test_paid_event_requires_payment(self):
        self.event.price = 500
        self.event.save(update_fields=["price"])

        with self.assertRaises(ValidationError):
            book_event(self.attendee1, self.event.pk)

    def test_cancellation_promotes_next_person(self):
        first = book_event(self.attendee1, self.event.pk)
        second = book_event(self.attendee2, self.event.pk)

        cancel_registration(self.attendee1, first.pk)

        first.refresh_from_db()
        second.refresh_from_db()

        self.assertEqual(
            first.status,
            Registration.Status.CANCELLED,
        )
        self.assertEqual(
            second.status,
            Registration.Status.CONFIRMED,
        )

    def test_waitlist_promotion_follows_order(self):
        first = book_event(self.attendee1, self.event.pk)
        second = book_event(self.attendee2, self.event.pk)
        third = book_event(self.attendee3, self.event.pk)

        cancel_registration(self.attendee1, first.pk)

        second.refresh_from_db()
        third.refresh_from_db()

        self.assertEqual(
            second.status,
            Registration.Status.CONFIRMED,
        )
        self.assertEqual(
            third.status,
            Registration.Status.WAITLISTED,
        )

    def test_cancelled_user_can_register_again(self):
        first = book_event(self.attendee1, self.event.pk)
        cancel_registration(self.attendee1, first.pk)

        new_registration = book_event(self.attendee1, self.event.pk)

        self.assertEqual(
            new_registration.status,
            Registration.Status.CONFIRMED,
        )

    def test_checked_in_booking_cannot_be_cancelled(self):
        registration = book_event(self.attendee1, self.event.pk)
        registration.checked_in_at = timezone.now()
        registration.save(update_fields=["checked_in_at"])

        with self.assertRaises(ValidationError):
            cancel_registration(self.attendee1, registration.pk)

    def test_capacity_cannot_be_reduced_below_confirmed_count(self):
        self.event.seat_limit = 2
        self.event.save(update_fields=["seat_limit"])

        book_event(self.attendee1, self.event.pk)
        book_event(self.attendee2, self.event.pk)

        self.event.seat_limit = 1

        with self.assertRaises(ValidationError):
            self.event.full_clean()

    def test_registration_endpoint_requires_post(self):
        self.client.force_login(self.attendee1)

        response = self.client.get(
            f"/bookings/events/{self.event.pk}/register/"
        )

        self.assertEqual(response.status_code, 405)

    def test_attendee_cannot_cancel_other_users_booking(self):
        registration = book_event(self.attendee1, self.event.pk)
        self.client.force_login(self.attendee2)

        response = self.client.post(
            f"/bookings/{registration.pk}/cancel/"
        )

        self.assertEqual(response.status_code, 404)