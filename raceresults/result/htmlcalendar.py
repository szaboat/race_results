from calendar import HTMLCalendar
import datetime

from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class RaceCalendar(HTMLCalendar):

    def __init__(self, races):
        super(RaceCalendar, self).__init__()
        self.races = self.group_by_date(races)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            _date = datetime.date(self.year, self.month, day)
            if _date in self.races:
                cssclass += ' filled'
                body = ['<ul>']
                for race in self.races[_date]:
                    body.append('<li><a href="{url}">'.format(type=race.type, url=race.get_absolute_url()))
                    body.append(esc(race.name))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month, withyear=None):
        self.year, self.month = year, month
        return super(RaceCalendar, self).formatmonth(year, month)

    def group_by_date(self, races):
        field = lambda race: race.date
        return dict(
                [(date, list(items)) for date, items in groupby(races, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)