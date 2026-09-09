from django import forms

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

        for name in ("start_at", "end_at"):
            self.fields[name].input_formats = ["%Y-%m-%dT%H:%M"]

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["category"].widget.attrs["class"] = "form-select"
        self.fields["status"].widget.attrs["class"] = "form-select"