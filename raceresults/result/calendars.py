from django_ical.views import ICalFeed

from .models import Race


class BaseRacesFeed(ICalFeed):
    product_id = '-//tekerem.hu//Example//EN'
    timezone = 'UTC'
    file_name = "calendar.ics"

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.url

    def item_start_datetime(self, item):
        return item.date

    def item_link(self, item):
        return item.get_absolute_url()


class AllRacesFeed(BaseRacesFeed):
    title = "tekerem.hu versenyek"

    def items(self):
        return Race.objects.filter(date__year=2017)
