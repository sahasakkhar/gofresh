from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from geopy import distance

from accounts.models import UserProfile
from customutils.custom_authentication import AppTokenAuthentication
from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from stores.models import Store, City
from stores.serializers import CityAreaListSerializer, StoreSerializer


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@authentication_classes((AppTokenAuthentication, ))
def find_store_with_location(request):

    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    radius = request.GET.get('radius')

    stores = Store.objects.all()
    nearest_stores_distance_list = []
    for store in stores:
        d = distance.distance((latitude, longitude), (store.position.latitude, store.position.longitude)).kilometers
        nearest_stores_distance_list.append({'distance': d, 'store': store})
    nearest_stores_distance_list = sorted(nearest_stores_distance_list, key=lambda k: k['distance'])
    nearest_stores_list = [nearest_stores_distance_list[i]['store'] for i in range(settings.NEAREST_STORE_LIMIT)]
    serializer = StoreSerializer(nearest_stores_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class CityViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = City.objects.all()
    serializer_class = CityAreaListSerializer
    authentication_classes = (AppTokenAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'area', 'is_active')


class StoreViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreSerializer
        elif self.action == 'retrieve':
            return StoreSerializer
        elif self.action == 'create':
            return StoreSerializer
        return StoreSerializer

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    authentication_classes = (AppTokenAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('city', 'area')

for_now = False

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@authentication_classes((AppTokenAuthentication, ))
def find_store(request):

    city = request.GET.get('city')
    area = request.GET.get('area')

    if for_now:
        serializer = StoreSerializer(Store.objects.all()[:1], context={"request": request}, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    stores = Store.objects.filter(Q(city=city) & Q(area=area) & Q(is_active=True))
    serializer = StoreSerializer(stores, many=True, context={"request": request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)