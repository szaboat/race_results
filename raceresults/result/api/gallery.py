from ..models import Gallery, Race
from rest_framework import routers, serializers, viewsets, mixins


class RaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Race
        fields = ('id', 'short_name', 'name', 'location', 'type', 'location', 'date')


class GallerySerializer(serializers.HyperlinkedModelSerializer):
    race = RaceSerializer()
    class Meta:
        model = Gallery
        fields = ('url', 'race', 'created_at')
        

class GalleryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class RaceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'gallery', GalleryViewSet)
router.register(r'races', RaceViewSet)