from django.forms import ModelForm
from .models import CalendarItem


class AddToCalendarForm(ModelForm):
    class Meta:
        model = CalendarItem
        fields = ['priority']
