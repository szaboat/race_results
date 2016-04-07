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
        race = Race.objects.get(pk=2)
        with open('../data/bonyhad16_veg.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                athlete, _ = Athlete.objects.get_or_create(name=row['Name'], uci_number=row['UCI'])
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
