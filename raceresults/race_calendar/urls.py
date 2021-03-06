from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<year>[0-9]{4})/(?P<name>[\w-]+)/add/$', views.add_to_calendar),
    url(r'your-races/$', views.your_races),
    url(r'athlete/(?P<athlete_id>[0-9]+)/calendar/$', views.athletes_calendar),
]
