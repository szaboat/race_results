from django.template.response import TemplateResponse
from .models import Race, Result, Athlete, Club


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

    return TemplateResponse(request, 'race.html', context)


def athlete_profile(request, athlete_id):
    athlete = Athlete.objects.get(id=athlete_id)
    results = Result.objects.filter(athlete=athlete)
    context = {
        'athlete': athlete,
        'results': results
    }

    return TemplateResponse(request, 'athlete.html', context)


def club_view(request, club_id):
    club = Club.objects.get(id=club_id)
    results = Result.objects.filter(club=club)
    context = {
        'results': results,
        'club': club
    }

    return TemplateResponse(request, 'club.html', context)
