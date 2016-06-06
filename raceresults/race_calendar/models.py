from django.db import models


class CalendarItem(models.Model):
    priority_choices = (
        ('A', 'A race'),
        ('B', 'B race'),
        ('C', 'C race'),
    )
    priority = models.CharField(choices=priority_choices, max_length=1)
    user = models.ForeignKey('auth.User')
    race = models.ForeignKey('result.Race', on_delete=models.SET_NULL, null=True)
