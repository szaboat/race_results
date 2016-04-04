from django.template.response import TemplateResponse
from .models import Race, Result


def race_view(request, year, name):
    race = Race.objects.get(short_name=name, date__year=year)

    context = {
        'race': race,
        'results' : Result.objects.filter(race=race)
    }
    return TemplateResponse(request, 'race_view.html', context)
