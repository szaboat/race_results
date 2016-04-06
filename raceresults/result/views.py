from django.template.response import TemplateResponse
from .models import Race, Result


def race_view(request, year, name):
    race = Race.objects.get(short_name=name, date__year=year)
    results = Result.objects.filter(race=race)
    categories = [category['category'] for category in results.values('category').distinct()]
    results_by_category = [
        {'results': Result.objects.filter(race=race, category=item), 'category': item } for item in categories
    ]
    context = {
        'race': race,
        'results' : results,
        'results_by_category': results_by_category
    }

    return TemplateResponse(request, 'race_view.html', context)
