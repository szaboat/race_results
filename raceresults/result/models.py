from __future__ import unicode_literals

import time

import datetime

from django.db import models

# Create your models here.


class Athlete(models.Model):
    name = models.CharField(max_length=30)
    year_of_birth = models.IntegerField(default=0)
    uci_number = models.CharField(max_length=20, null=True, blank=True)


class Club(models.Model):
    name = models.CharField(max_length=255)


class Lap(models.Model):
    time = models.IntegerField()
    result = models.ForeignKey('Result')


class Race(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=30)
    url = models.URLField()
    date = models.DateField()
    type_choices = (
        ('XCO', 'Olymic Cross Country'),
        ('CX', 'Cyclocross'),
        ('XCM', 'Cross Country Marathon'),
        ('ROAD', 'Road race'),
        ('XCU', 'Cross Country Ultra'),
        ('TOUR', 'Tour'),
    )
    type = models.CharField(max_length=4, choices=type_choices)
    location = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    @property
    def days_to_race(self):
        delta = self.date - datetime.date.today()
        return delta.days

    def get_absolute_url(self):
        return "/{year}/{name}/".format(year=self.date.year, name=self.short_name)

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
    race = models.ForeignKey('Race')
    club = models.ForeignKey('Club', null=True, blank=True)
    total_time = models.IntegerField()
    position = models.IntegerField()
    race_number = models.CharField(max_length=5)
    imported_at = models.DateTimeField()
    category = models.CharField(max_length=20, null=True, blank=True)

    @property
    def time(self):
        if self.total_time != -1:
            m, s = divmod(self.total_time, 60)
            h, m = divmod(m, 60)
            return '%s:%s:%s' % (h,m,s)
