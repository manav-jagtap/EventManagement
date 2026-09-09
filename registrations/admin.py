from django.contrib import admin

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event",
        "status",
        "checked_in_at",
        "created_at",
    )
    list_filter = ("status", "checked_in_at", "event")
    search_fields = ("user__username", "event__title", "ticket_code")
    readonly_fields = ("ticket_code", "created_at", "checked_in_at")
    list_select_related = ("user", "event")
