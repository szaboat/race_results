import datetime

from django.apps import apps
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe

from .models import Race, Result, Athlete, Club
from .htmlcalendar import RaceCalendar

CalendarItem = apps.get_model('race_calendar.CalendarItem')  # WTF?


def race_view(request, year, name):
    race = Race.objects.get(short_name=name, date__year=year)
    results = Result.objects.filter(race=race)
    categories = [category['category'] for category in results.values('category').distinct()]
    results_by_category = [
        {'results': Result.objects.filter(race=race, category=item), 'category': item } for item in categories
    ]

    if request.user.is_authenticated():
        race_is_in_calendar = len(CalendarItem.objects.filter(race=race, user=request.user))
    else:
        race_is_in_calendar = None
    context = {
        'race': race,
        'results' : results,
        'results_by_category': results_by_category,
        'race_is_in_calendar': race_is_in_calendar
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


def races_view(request, filter=None):
    if filter == 'all':
        races = Race.objects.all().order_by('date')
    elif filter:
        races = Race.objects.filter(type=filter.upper()).order_by('date')
    else:
        races = Race.objects.filter(date__gte=datetime.date.today()).order_by('date')

    race_types = Race.type_choices
    context = {
        'races': races,
        'types': race_types
    }
    return TemplateResponse(request, 'races.html', context)


def calendar(request):
    races = Race.objects.order_by('date').filter(date__year=2016)
    cal = RaceCalendar(races).formatyear(theyear=2016, width=1)
    return TemplateResponse(request, 'calendar.html', {'calendar': mark_safe(cal),})