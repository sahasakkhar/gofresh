from products.models import Category
from products.serializers import CategorySerializer
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from customutils.custom_authentication import AppTokenAuthentication
from stores.models import City
from stores.serializers import CityAreaListSerializer


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_initial_information(request):

    cities = City.objects.all()
    city_serializer = CityAreaListSerializer(cities, many=True)
    categories = Category.objects.all()
    category_serializer = CategorySerializer(categories, many = True)
    data = {}
    data['city'] = city_serializer.data
    data['category'] = category_serializer.data
    return Response(data=data, status=status.HTTP_200_OK)