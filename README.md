# EventHub — Event Management & Digital Ticketing Platform

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=black)](https://render.com/)

EventHub is a web-based event management platform built with Django.

The system allows attendees to discover events, register for available seats, join waitlists, receive digital QR tickets, manage bookings, and attend events through organizer-controlled ticket verification and check-in.

Organizers can create and manage events, monitor registrations, verify tickets, check attendees in, and view event analytics. Administrators manage users, categories, events, registrations, and platform data through Django Admin.

---

## Key Features

### Event Discovery

- Browse upcoming published events
- Search events by title, description, venue, city, or category
- Filter events by category
- Filter events by city
- View complete event information
- View available seats
- View related events from the same category
- Responsive event cards and event detail pages

### Attendee Accounts

- User registration and login
- Public signup creates attendee accounts
- Secure authentication using Django's built-in authentication system
- Personal attendee dashboard
- Separate attendee permissions from organizer and administrator roles

### Event Registration

- Register for free published events
- Automatic seat availability checking
- Confirmed registration when seats are available
- Automatic waitlist when the event is full
- Duplicate active registration protection
- Paid events are currently blocked until payment support is added

### Waitlist Management

- Automatic waitlist creation when event capacity is reached
- FIFO waitlist order
- Automatic promotion of the next waitlisted attendee when a confirmed booking is cancelled
- Seat count remains protected during registration and cancellation operations

### Booking Management

- View personal registrations
- Check booking status
- Cancel eligible registrations
- Cancelled users may register again
- Checked-in registrations cannot be cancelled
- Cancellation is blocked after the event starts

### Digital Ticketing

- Unique UUID ticket generated for every registration
- QR code generated for confirmed tickets
- Personal digital ticket page
- QR data linked to the unique ticket identifier
- Ticket access restricted to the registered attendee

### Organizer Dashboard

- Separate organizer role
- Create new events
- Edit owned events
- Delete events without registrations
- Prevent deletion of events that already contain registrations
- Cancel events when deletion is not appropriate
- View organizer-specific events only

### Ticket Verification & Check-In

- Verify tickets using unique ticket IDs
- Organizers can verify tickets only for their own events
- Administrators can verify tickets across the platform
- Only confirmed registrations can be checked in
- Duplicate check-in protection
- Check-in timestamp stored in the database

### Event Analytics

- Total events
- Total registrations
- Confirmed registrations
- Waitlisted registrations
- Checked-in attendees
- Attendance percentage
- Per-event analytics
- Chart.js based registration and check-in visualization

### Administration

- Django Admin panel
- Manage users
- Manage user roles
- Manage categories
- Manage events
- Manage registrations
- Search and filter administrative records

### User Interface

- Modern dark event-platform design
- Responsive layout
- Bootstrap-based interface
- Bootstrap Icons
- Django Templates
- HTML and CSS
- Lightweight Vanilla JavaScript
- Chart.js for analytics

---

## Technology Stack

- **Programming Language:** Python 3.13
- **Backend Framework:** Django 6.1
- **Frontend:** HTML5, CSS3, Bootstrap, Django Templates, Vanilla JavaScript
- **Database:** SQLite
- **ORM:** Django ORM
- **QR Generation:** qrcode
- **Image Handling:** Pillow
- **Static File Serving:** WhiteNoise
- **Production Server:** Gunicorn
- **Analytics:** Chart.js
- **Deployment Platform:** Render
- **Version Control:** Git and GitHub

---

## Project Structure

```text
EventManagement/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── events/
│   ├── management/
│   │   └── commands/
│   │       ├── bootstrap_demo.py
│   │       └── seed_demo_events.py
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── registrations/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── demo_banners/
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
