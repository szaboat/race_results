from django.apps import apps
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from .models import CalendarItem
from .forms import AddToCalendarForm

Race = apps.get_model('result.Race')  # WTF?


def add_to_calendar(request, year, name):
    if request.user.is_authenticated():
        race = Race.objects.get(short_name=name, date__year=year)
        if request.method == "POST":
            form = AddToCalendarForm(request.POST)
            if form.is_valid():
                CalendarItem.objects.create(
                    user=request.user,
                    race=race,
                    priority=form.cleaned_data['priority']
                )
                return HttpResponseRedirect('/')
        else:
            form = AddToCalendarForm(initial={'priority': 'B'})
            return TemplateResponse(request, 'add_to_calendar.html', {'form': form, 'race': race})

    else:
        return HttpResponseBadRequest()


def athletes_calendar(request, athlete_id):
    try:
        user = User.objects.get(pk=athlete_id)
    except User.DoesNotExist:
        return HttpResponseRedirect('/')

    items = CalendarItem.objects.filter(user=user)
    races = [item.race for item in items]
    races_sorted_by_date = sorted(races, key=lambda x: x.date)

    context = {
        'races': races_sorted_by_date,
        'athlete_user': User.objects.get(pk=user.id)
    }

    return TemplateResponse(request, 'athlete_races.html', context)

def your_races(request):
    items = CalendarItem.objects.filter(user=request.user)
    races = [item.race for item in items]
    context = {
        'races': races,
    }

    return TemplateResponse(request, 'your_races.html', context)
