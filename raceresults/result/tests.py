#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime
import time

from django.test import TestCase

# Create your tests here.
from .helpers import get_time_in_seconds
from .models import Athlete, Club, Race, Lap, Result


class AthleteModelTestCase(TestCase):
    def test_cruds(self):
        athlete = Athlete.objects.create(name='Denes Arvay', year_of_birth=1981)
        expected_result = Athlete.objects.get(pk=1)
        self.assertEqual(athlete, expected_result)


class ClubModelTestCase(TestCase):
    def test_cruds(self):
        club = Club.objects.create(name='Meditech')
        expected_club = Club.objects.get(pk=1)
        self.assertEqual(club, expected_club)


class ResultModelTestCase(TestCase):
    def test_cruds(self):
        athlete = Athlete.objects.create(name='Denes Arvay', year_of_birth=1981)

        race = Race.objects.create(name='Salzkammergut Trophy', date=datetime.date.today())
        result = Result.objects.create(race=race, athlete=athlete, total_time=1231, position=200, imported_at=datetime.date.today())

        lap1 = Lap.objects.create(time=15 * 60, result=result)
        lap2 = Lap.objects.create(time=13 * 60, result=result)

        expected_result = Result.objects.get(pk=result.id)
        self.assertEqual(result, expected_result)
        self.assertEqual(result.lap_set.all()[0], lap1)
        self.assertEqual(result.lap_set.all()[1], lap2)


class TestViews(TestCase):
    def test_race_page(self):
        Race.objects.create(name="Matramaraton", short_name="matramaraton", url="http://topmaraton.hu", date=datetime.date(2015,8,30), type='XCM', location="Matrahaza")
        response = self.client.get('/2015/matramaraton/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matramaraton")


class CSVLoadTestCase(TestCase):
    def test(self):
        """
            [ ] TODO status
            [ ] TODO category
        """
        race = Race.objects.create(name="Bonyhad", short_name="bonyhad", url="http://akarmi.hu", date=datetime.date(2016,04,03), type='ROAD', location="Bonyhad")
        with open('../data/bonyhad16_veg.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                athlete = Athlete.objects.create(name=row['Name'], uci_number=row['UCI'])
                club = Club.objects.create(name=row['Club'])

                if row['Result'] == 'DNF' or row['Result'] == '':
                    time_in_seconds = -1
                    position = -1
                else:
                    time_in_seconds = get_time_in_seconds(row['Time'])
                    position = row['Result']

                Result.objects.create(race=race, club=club, athlete=athlete,
                                      total_time=time_in_seconds, position=position,
                                      race_number=row['Number'], imported_at=datetime.date.today(),
                                      category=row['Cat'].strip())
