# EventHub — Event Management & Digital Ticketing

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=black)](https://eventmanagement-8ndb.onrender.com)

EventHub is a deployed Django application for event discovery, capacity-aware registration, FIFO waitlisting, QR ticketing, organizer check-in, and attendance analytics.

[Open Live Demo](https://eventmanagement-8ndb.onrender.com) • [View Source](https://github.com/manav-jagtap/EventManagement)

## Engineering Highlights

- Custom attendee, organizer, and administrator roles
- Transaction-based registration and cancellation
- Automatic FIFO waitlist promotion
- UUID-based QR tickets
- Organizer ownership and attendee access checks
- Duplicate registration and check-in prevention
- Capacity validation and protected event deletion
- Automated tests for critical booking rules

## Core Features

### Attendees

- Browse, search, and filter published events
- Register for available seats or join a waitlist
- Access personal bookings and QR tickets
- Cancel eligible registrations

### Organizers

- Create and manage owned events
- Verify ticket IDs and check attendees in
- Monitor registrations and attendance analytics

### Administrators

- Manage users, roles, categories, events, and registrations through Django Admin

## Registration Workflow

1. An attendee opens a published upcoming event.
2. EventHub checks eligibility and active registrations.
3. Available capacity creates a confirmed booking and QR ticket.
4. A full event creates a waitlisted booking.
5. Cancellation promotes the oldest eligible waitlisted attendee.

## Important Business Rules

- Events must start in the future and end after their start time.
- Capacity cannot be reduced below confirmed registrations.
- Only published upcoming events accept registrations.
- Duplicate active registrations are blocked.
- Checked-in bookings cannot be cancelled.
- Only confirmed tickets can be checked in.
- Organizers can manage and verify only their own events.
- Events with registrations cannot be directly deleted.

## Technology Stack

- Python 3.13 and Django 6.1
- HTML, CSS, Bootstrap, Django Templates, JavaScript
- SQLite and Django ORM
- qrcode, Pillow, and Chart.js
- WhiteNoise, Gunicorn, and Render

## Project Structure

```text
EventManagement/
├── accounts/          # Authentication and role-based dashboards
├── events/            # Events, categories, search, and analytics
├── registrations/     # Bookings, waitlist, tickets, and check-in
├── config/            # Django configuration
├── demo_banners/      # Demo event images
├── manage.py
├── requirements.txt
└── README.md
```

## Run Locally

```bash
git clone https://github.com/manav-jagtap/EventManagement.git
cd EventManagement
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Tests

```bash
python manage.py test
```

Automated tests cover confirmation, waitlisting, duplicate prevention, cancellation, FIFO promotion, capacity validation, and access control.

## Security

- Django password hashing and validation
- Role- and ownership-based access control
- CSRF protection and POST-only sensitive actions
- UUID tickets and duplicate-booking constraints
- Secrets stored through environment variables
- `.env` and `db.sqlite3` excluded from Git

## Deployment Note

The Render demo currently uses SQLite. Render's free-service filesystem is not intended for permanent SQLite persistence, so runtime accounts and bookings may be reset after redeployment or instance replacement. Demo bootstrap commands recreate the required sample data. A production implementation should use managed PostgreSQL and persistent media storage.

## Planned Enhancements

- PostgreSQL production database
- Persistent cloud media storage
- Payment and email-confirmation workflows
- QR scanner support
- Reviews, notifications, and attendee exports

## Author

**Manav Jagtap** — B.Sc. Computer Science student
