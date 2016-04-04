import csv

import datetime

from django.core.management.base import BaseCommand, CommandError
from ...models import Race, Club, Athlete, Result
from ...helpers import get_time_in_seconds


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
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
