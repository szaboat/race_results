from __future__ import unicode_literals

import datetime

from django.db import models
from django_countries.fields import CountryField


class Athlete(models.Model):
    name = models.CharField(max_length=30)
    year_of_birth = models.IntegerField(default=0)
    uci_number = models.CharField(max_length=20, null=True, blank=True)


class Club(models.Model):
    name = models.CharField(max_length=255)


class Lap(models.Model):
    time = models.IntegerField()
    result = models.ForeignKey('Result')


YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))


class Series(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField('year', max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __unicode__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=30)
    url = models.URLField()
    date = models.DateField()
    type_choices = (
        ('XCO', 'Olymic Cross Country'),
        ('CX', 'Cyclocross'),
        ('END', 'Enduro'),
        ('XCM', 'Cross Country Marathon'),
        ('MTBO', 'MTB Orienteering'),
        ('ROAD', 'Road race'),
        ('XCU', 'Cross Country Ultra'),
        ('TOUR', 'Tour'),
        ('ETC', 'Other'),
    )
    type = models.CharField(max_length=4, choices=type_choices)
    location = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    series = models.ForeignKey(Series, null=True, blank=True)
    country = CountryField(max_length=2, null=True, blank=True)

    @property
    def days_to_race(self):
        delta = self.date - datetime.date.today()
        return delta.days

    def get_absolute_url(self):
        return "/{year}/{name}/".format(year=self.date.year, name=self.short_name)

    @property
    def galleries(self):
        return Gallery.objects.filter(race=self.id)

    def __unicode__(self):
        return "{short_name} /  {date} / {type}".format(short_name=self.name, date=self.date, type=self.type)


class Result(models.Model):
    status_types = (
        ('FIN', 'Finished'),
        ('DNF', 'Did not finish'),
        ('DSQ', 'Disqualified'),
        ('DNS', 'Did not start'),
    )
    status = models.CharField(choices=status_types, max_length=3)
    athlete = models.ForeignKey('Athlete')
    race = models.ForeignKey('Race', on_delete=models.SET_NULL, null=True, blank=True)
    club = models.ForeignKey('Club', null=True, blank=True)
    total_time = models.IntegerField()
    position = models.IntegerField()
    race_number = models.CharField(max_length=5)
    imported_at = models.DateTimeField()
    category = models.CharField(max_length=20, null=True, blank=True)
    cohort = models.CharField(max_length=10)

    @property
    def time(self):
        if self.total_time != -1:
            m, s = divmod(self.total_time, 60)
            h, m = divmod(m, 60)
            return '%s:%s:%s' % (h,m,s)


class Gallery(models.Model):
    url = models.URLField()
    race = models.ForeignKey('Race')
    created_at = models.DateTimeField(auto_now_add=True)