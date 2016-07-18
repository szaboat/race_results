import datetime

from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase

from ..models import CalendarItem
from autofixture import AutoFixture

Race = apps.get_model('result.Race')  # WTF?


class CalendarItemModelTestCase(TestCase):
    def test_cruds(self):
        user = User.objects.create()
        race = Race.objects.create(name='Salzkammergut Trophy', date=datetime.date.today())
        item = CalendarItem.objects.create(race=race, user=user, priority='A')

        self.assertEqual(item, CalendarItem.objects.get(pk=1))


class AthleteCalendarTestCase(TestCase):
    def test_athletes_races_are_sorted(self):
        race_fixture = AutoFixture(Race)
        races = race_fixture.create(10)
        user = User.objects.create()
        for race in races:
            CalendarItem.objects.create(race=race, user=user, priority='A')

        AutoFixture(CalendarItem, {user:user})

        response = self.client.get('/athlete/{id}/calendar/'.format(id=user.id))

        races = response.context_data['races']
        races_sorted = sorted(races, key=lambda x: x.date)
        self.assertListEqual(races, races_sorted)
