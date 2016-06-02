import datetime

from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase

from ..models import CalendarItem
Race = apps.get_model('result.Race')  # WTF?


class CalendarItemModelTestCase(TestCase):
    def test_cruds(self):
        user = User.objects.create()
        race = Race.objects.create(name='Salzkammergut Trophy', date=datetime.date.today())
        item = CalendarItem.objects.create(race=race, user=user, priority='A')

        self.assertEqual(item, CalendarItem.objects.get(pk=1))
