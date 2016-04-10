#!/usr/bin/python
# -*- coding: utf-8
import csv

import datetime

from django.core.management.base import BaseCommand
from ...models import Race, Club, Athlete, Result
from ...helpers import get_time_in_seconds


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        race = Race.objects.create(name="XXV. Stop cukrászda időfuam - Tarján, 2016.04.10.", short_name="stop-cukraszda", date=datetime.date.today(), type='ROAD',  location="Tarján", url="http://velo.hu/2016/stop-cukraszda-idofutam.html")
        with open('../data/stop_cukraszda_2016.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                athlete, _ = Athlete.objects.get_or_create(name=row['Name'])
                club, _ = Club.objects.get_or_create(name=row['Club'])

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
