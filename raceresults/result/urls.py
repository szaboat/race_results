from django.conf.urls import url, include

from .calendars import AllRacesFeed
from . import views

urlpatterns = [
    url(r'^(?P<year>[0-9]{4})/(?P<name>[\w-]+)/$', views.race_view),
    url(r'^athlete/(?P<athlete_id>[0-9]+)/$', views.athlete_profile),
    url(r'^club/(?P<club_id>[0-9]+)/$', views.club_view),
    url(r'^calendar/$', views.calendar),

    # feeds
    url(r'^races/all/calendar.ics$', AllRacesFeed()),

    url(r'^races/(?P<filter>[a-z]+)/', views.races_view),
    url(r'^pages/', include('django.contrib.flatpages.urls')),


    url(r'^', views.races_view),
]