EventHub Demo Seed Package

Contains:
- events/management/commands/seed_demo_events.py
- demo_banners/ with 10 generated event banner images

How to use:
1. Copy the folder:
   events/management/commands/
   into your EventManagement project's events app.

2. Copy:
   demo_banners/
   into the project root:
   D:\project\EventManagement\demo_banners\

3. Make sure Organizer01 and Organizer02 already exist and both have role='organizer'.

4. Run:
   python manage.py seed_demo_events

5. Open:
   http://127.0.0.1:8000/events/

Notes:
- Uses update_or_create(), so rerunning updates the same demo events instead of creating duplicates.
- All 10 demo events are published and currently free so your existing registration flow works.
- Events are split between Organizer01 and Organizer02 for realistic analytics and ownership testing.
