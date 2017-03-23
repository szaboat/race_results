#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime

import icalendar
from django.test import RequestFactory
from django.test import TestCase
from six import b

from .helpers import get_time_in_seconds
from .models import Athlete, Club, Race, Lap, Result, Series, Gallery


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


class RaceSeriesTestCase(TestCase):
    def test_series_model(self):
        cyclocross_hu = Series.objects.create(name="cyclocross.hu", year=2016)
        self.assertEqual(Series.objects.all()[0], cyclocross_hu)

    def test_relations(self):
        cyclocross_hu = Series.objects.create(name="cyclocross.hu", year=2016)
        Race.objects.create(name="Crossliget", short_name='crossliget', url="http://crossliget.hu", date=datetime.date(2015,8,30), type='CX', location="Varosliget", series=cyclocross_hu)
        Race.objects.create(name="Veszprem", short_name='veszprem cx', url="http://vesz.hu", date=datetime.date(2015,8,30), type='CX', location="Veszprem", series=cyclocross_hu)

        races = Race.objects.filter(series=cyclocross_hu)

        self.assertEqual(races[0].series, cyclocross_hu)
        self.assertEqual(races[1].series, cyclocross_hu)


class TestViews(TestCase):
    def test_race_page(self):
        Race.objects.create(name="Matramaraton", short_name="matramaraton", url="http://topmaraton.hu", date=datetime.date(2015,8,30), type='XCM', location="Matrahaza")
        response = self.client.get('/2015/matramaraton/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matramaraton")

    def test_index_page_should_list_races_from_today(self):
        Race.objects.create(name="Matramaraton", short_name="matramaraton", url="http://topmaraton.hu", date=datetime.date.today(), type='XCM', location="Matrahaza")
        Race.objects.create(name="Duna maraton", short_name="matramaraton", url="http://topmaraton.hu", date=datetime.date.today() + datetime.timedelta(days=20), type='XCM', location="Matrahaza")

        response = self.client.get('/', follow=True)
        self.assertEqual(len(response.context_data['races']), 2)


class TestGallery(TestCase):
    def test_model(self):
        race = Race.objects.create(name="Matramaraton", short_name="matramaraton", url="http://topmaraton.hu", date=datetime.date(2015,8,30), type='XCM', location="Matrahaza")
        gallery = Gallery.objects.create(url='https://facebook.com/gallery', race=race)

        assert gallery.url == 'https://facebook.com/gallery'
        assert gallery.race == race


class TestGalleryRaceConnection(TestCase):
    def test_connection(self):
        race = Race.objects.create(name="Matramaraton", short_name="matramaraton", url="http://topmaraton.hu", date=datetime.date(2015,8,30), type='XCM', location="Matrahaza")
        gallery = Gallery.objects.create(url='https://facebook.com/gallery', race=race)
        gallery2 = Gallery.objects.create(url='https://facebook.com/gallery2', race=race)

        self.assertEqual(race.galleries[0], gallery)
        self.assertEqual(race.galleries[1], gallery2)


class TestCalendarView(TestCase):
    def setUp(self):
        Race.objects.create(name="Matramaraton", short_name="matramaraton", url="http://topmaraton.hu",
                            date=datetime.date(2017, 8, 30), type='XCM', location="Matrahaza")
        Race.objects.create(name="Crosskovacsi XCO", short_name="crosskovacsi", url="http://crosskovacsi.hu",
                            date=datetime.date(2017, 8, 31), type='XCO', location="Nagykovacsi")

    def test_all_calendar(self):
        response = self.client.get('/races/all/calendar.ics')

        calendar_feed = icalendar.Calendar.from_ical(response.content)
        self.assertEqual(calendar_feed['X-WR-CALNAME'], 'tekerem.hu versenyek')

    def test_all_calendar_items(self):
        response = self.client.get('/races/all/calendar.ics')

        calendar_feed = icalendar.Calendar.from_ical(response.content)

        self.assertEqual(len(calendar_feed.subcomponents), 2)
        self.assertEqual(calendar_feed['X-WR-CALNAME'], 'tekerem.hu versenyek')
        self.assertEqual(calendar_feed.subcomponents[0]['SUMMARY'], 'Matramaraton')
        self.assertEqual(calendar_feed.subcomponents[0]['DESCRIPTION'], 'http://topmaraton.hu')
        self.assertEqual(calendar_feed.subcomponents[0]['DTSTART'].to_ical(), b('20170830'))

    def test_filtered_feed(self):
        response = self.client.get('/races/xcm/calendar.ics')

        calendar_feed = icalendar.Calendar.from_ical(response.content)

        self.assertEqual(len(calendar_feed.subcomponents), 1)
        self.assertEqual(calendar_feed['X-WR-CALNAME'], 'tekerem.hu XCM versenyek')
        self.assertEqual(calendar_feed.subcomponents[0]['SUMMARY'], 'Matramaraton')
        self.assertEqual(calendar_feed.subcomponents[0]['DESCRIPTION'], 'http://topmaraton.hu')
        self.assertEqual(calendar_feed.subcomponents[0]['DTSTART'].to_ical(), b('20170830'))

    def test_filtered_feed_different_type(self):
        response = self.client.get('/races/xco/calendar.ics')

        calendar_feed = icalendar.Calendar.from_ical(response.content)

        self.assertEqual(len(calendar_feed.subcomponents), 1)
        self.assertEqual(calendar_feed['X-WR-CALNAME'], 'tekerem.hu XCO versenyek')
        self.assertEqual(calendar_feed.subcomponents[0]['SUMMARY'], 'Crosskovacsi XCO')
        self.assertEqual(calendar_feed.subcomponents[0]['DESCRIPTION'], 'http://crosskovacsi.hu')
        self.assertEqual(calendar_feed.subcomponents[0]['DTSTART'].to_ical(), b('20170831'))


class CSVLoadTestCase(TestCase):
    def test(self):
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
