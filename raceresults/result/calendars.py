from django_ical.views import ICalFeed

from .models import Race


class BaseRacesFeed(ICalFeed):
    product_id = '-//tekerem.hu//Example//EN'
    timezone = 'UTC'
    file_name = "calendar.ics"
    filter = 'all'

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.url

    def item_start_datetime(self, item):
        return item.date

    def item_link(self, item):
        return item.get_absolute_url()

    def get_object(self, request, *args, **kwargs):
        super(BaseRacesFeed, self).get_object(request, *args, **kwargs)
        self.filter = kwargs.get('filter', 'all').upper()


class AllRacesFeed(BaseRacesFeed):
    title = "tekerem.hu versenyek"

    def items(self):
        return Race.objects.filter(date__year=2017)


class FilteredRacesFeed(BaseRacesFeed):
    @property
    def title(self):
        return 'tekerem.hu {filter} versenyek'.format(filter=self.filter)

    def items(self):
        return Race.objects.filter(date__year=2017, type=self.filter)
