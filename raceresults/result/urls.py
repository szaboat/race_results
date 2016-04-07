from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<year>[0-9]{4})/(?P<name>[\w-]+)/$', views.race_view),
    url(r'^athlete/(?P<athlete_id>[0-9]+)/$', views.athlete_profile),
]