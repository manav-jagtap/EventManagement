from django import forms
from django.utils import timezone

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "category",
            "title",
            "description",
            "banner",
            "venue",
            "address",
            "city",
            "start_at",
            "end_at",
            "price",
            "seat_limit",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "address": forms.Textarea(attrs={"rows": 2}),
            "start_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_at"].input_formats = ["%Y-%m-%dT%H:%M"]

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

        self.fields["category"].widget.attrs["class"] = "form-select"
        self.fields["status"].widget.attrs["class"] = "form-select"

    def clean_start_at(self):
        start_at = self.cleaned_data["start_at"]
        if not self.instance.pk and start_at < timezone.now():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start_at