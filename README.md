# EventHub — Event Management & Digital Ticketing Platform

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=black)](https://render.com/)

EventHub is a Django-based event management platform for attendees, organizers, and administrators.

Attendees can discover events, register for available seats, join a waitlist when an event is full, manage bookings, and access QR-based digital tickets. Organizers can create and manage events, verify tickets, check attendees in, and monitor event performance through analytics.

---

## Key Features

### Event Discovery

- Browse upcoming published events
- Search by event name, description, venue, city, or category
- Filter events by category and city
- View event details, available seats, and related events

### Attendee Accounts

- User registration and login
- Secure Django authentication
- Personal attendee dashboard
- View registrations and booking status

### Event Registration

- Register for free published events
- Automatic confirmed booking when seats are available
- Automatic waitlist when the event is full
- Duplicate active registration protection
- Cancel eligible bookings
- Re-register after cancellation when allowed

### Waitlist Management

- FIFO waitlist order
- Automatic promotion when a confirmed attendee cancels
- Capacity-aware booking logic
- Transaction-based registration and cancellation flow

### Digital Tickets

- Unique UUID ticket for every registration
- QR code generation for confirmed tickets
- Personal digital ticket page
- Ticket access restricted to the registered attendee

### Organizer Dashboard

- Create events
- Edit owned events
- Manage event status
- Delete events only when no registrations exist
- View organizer-specific events

### Ticket Verification & Check-In

- Verify attendee ticket IDs
- Organizer access limited to owned events
- Check in confirmed attendees
- Prevent duplicate check-ins
- Store check-in date and time

### Event Analytics

- Total events
- Total registrations
- Confirmed registrations
- Waitlisted registrations
- Checked-in attendees
- Attendance percentage
- Chart.js visualizations

### Administration

- Django Admin panel
- Manage users and roles
- Manage categories
- Manage events
- Manage registrations

---

## Technology Stack

- **Programming Language:** Python 3.13
- **Backend Framework:** Django 6.1
- **Frontend:** HTML5, CSS3, Bootstrap, Django Templates, Vanilla JavaScript
- **Database:** SQLite
- **ORM:** Django ORM
- **QR Code Generation:** qrcode
- **Image Handling:** Pillow
- **Analytics:** Chart.js
- **Static File Serving:** WhiteNoise
- **Production Server:** Gunicorn
- **Deployment Platform:** Render
- **Version Control:** Git and GitHub

---

## Project Structure

```text
EventManagement/
│
├── accounts/          # Authentication, custom user model and role-based dashboard
├── events/            # Event management, categories, search, filters and analytics
├── registrations/     # Booking, waitlist, QR tickets, cancellation and check-in
├── config/            # Django settings, root URLs and deployment configuration
├── demo_banners/      # Demo event banner images
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

The project follows Django's app-based structure so each major responsibility stays separated and easy to maintain.

---

## User Roles

### Attendee

- Create an account and login
- Explore events
- Search and filter events
- Register for events
- Receive confirmed or waitlisted status
- View bookings
- Access QR tickets
- Cancel eligible registrations

### Organizer

- Access organizer dashboard
- Create and manage owned events
- Verify attendee tickets
- Check attendees in
- View event analytics

### Administrator

- Access Django Admin
- Manage users and roles
- Manage categories, events, and registrations
- Perform platform-wide administration

---

## Registration Workflow

```text
Attendee
   │
   ▼
Explore Events
   │
   ▼
Open Event Details
   │
   ▼
Register
   │
   ▼
Check Seat Availability
   │
   ├── Seat Available ──► Confirmed ──► Digital QR Ticket
   │
   └── Event Full ──────► Waitlisted
```

When a confirmed attendee cancels, the oldest waitlisted attendee is automatically promoted to confirmed status.

---

## Ticket Check-In Workflow

```text
Confirmed Registration
        │
        ▼
Unique Ticket UUID
        │
        ▼
QR Code Generated
        │
        ▼
Organizer Verifies Ticket
        │
        ▼
Attendee Checked In
        │
        ▼
Check-In Time Stored
```

---

## Database Models

### User

Custom Django user model with three roles:

- Admin
- Organizer
- Attendee

### Category

Stores event categories such as Technology, Music, Sports, Workshop, Education, Gaming, Photography, and others.

### Event

Stores event details including organizer, category, title, description, banner, venue, city, schedule, price, seat limit, and event status.

Event statuses:

- Draft
- Published
- Cancelled

### Registration

Stores attendee booking information, event reference, unique ticket UUID, booking status, check-in time, and creation time.

Registration statuses:

- Confirmed
- Waitlisted
- Cancelled

---

## Important Business Rules

- New events must start in the future
- Event end time must be after the start time
- Seat capacity cannot be reduced below confirmed registrations
- Only published upcoming events accept registrations
- Only attendee accounts can register
- Duplicate active registrations are blocked
- Checked-in bookings cannot be cancelled
- Cancellation is blocked after the event starts
- Only confirmed registrations can be checked in
- Organizers can manage and verify only their own events
- Events with registrations cannot be directly deleted

---

## Running the Application Locally

### Clone the Repository

```bash
git clone https://github.com/manav-jagtap/EventManagement.git
cd EventManagement
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Database Migrations

```bash
python manage.py migrate
```

### Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Running Tests

```bash
python manage.py test
```

The project includes automated registration tests for booking confirmation, waitlisting, duplicate booking prevention, cancellation, FIFO promotion, capacity validation, and access control.

---

## Production Deployment

EventHub is deployed on Render using:

- **Render** for web application hosting
- **Gunicorn** as the production WSGI server
- **WhiteNoise** for static file serving
- **SQLite** as the current demo database
- **Environment variables** for sensitive configuration

Deployment flow:

```text
GitHub
   │
   ▼
Render
   │
   ▼
Install Dependencies
   │
   ▼
Collect Static Files
   │
   ▼
Apply Migrations
   │
   ▼
Bootstrap Demo Data
   │
   ▼
Start Django with Gunicorn
```

---

## Demo Data

The project includes Django management commands for creating the demo setup used during deployment.

The current demo includes:

- 1 administrator account
- 2 organizer accounts
- 16 sample events
- Multiple event categories
- Events across multiple Maharashtra cities

Passwords and secret values are stored in environment variables and are not committed to GitHub.

---

## Security

- Django authentication and password hashing
- Password validation
- Role-based access control
- CSRF protection
- Secure cookies in production
- Organizer ownership checks
- Attendee ownership checks
- POST-only sensitive actions
- Unique ticket UUIDs
- Duplicate active registration database constraint
- Secret values stored in environment variables
- `.env` and `db.sqlite3` excluded from Git

---

## SQLite Deployment Note

The current Render deployment intentionally uses SQLite because EventHub is used as a portfolio, academic, and demonstration project.

Render's free web service filesystem is not intended for permanent SQLite persistence. Runtime data such as new attendee accounts, bookings, cancellations, and check-ins may be lost after some redeployments or instance resets.

The demo bootstrap command recreates the required administrator, organizers, categories, and sample events during deployment.

For a real production system with permanent user data, the database can be migrated to managed PostgreSQL.

---

## Use Cases

- College event management
- Workshop registration
- Conference registration
- Community event management
- Sports event registration
- Academic Django project
- Full-stack portfolio project

---

## Future Enhancements

- PostgreSQL production database
- Persistent cloud media storage
- Online payment gateway
- Paid event booking
- Email booking confirmations
- Automated ticket delivery
- QR scanner support
- Event reviews and ratings
- Notifications and reminders
- Advanced organizer analytics
- Exportable attendee lists

---

## Project Status

EventHub currently includes the complete attendee registration flow, organizer event management, automatic waitlisting, QR ticketing, ticket verification, attendee check-in, organizer analytics, Django Admin integration, automated booking tests, GitHub version control, and Render deployment.


**Live Application:** [https://eventmanagement-8ndb.onrender.com](https://eventmanagement-8ndb.onrender.com)

---

## Author

**Manav Jagtap**  
B.Sc. Computer Science

If you find the project useful, consider giving it a star on GitHub.
