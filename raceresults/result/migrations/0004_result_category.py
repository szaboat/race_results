# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0003_athlete_uci_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
