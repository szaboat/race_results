from django.template.response import TemplateResponse
from .models import Race


def race_view(request, year, name):
    race = Race.objects.get(short_name=name, date__year=year)
    return TemplateResponse(request, 'race_view.html', {'race': race})
