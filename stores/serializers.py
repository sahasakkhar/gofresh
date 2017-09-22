from rest_framework import serializers
from stores.models import Store, City, Area


class AreaInsideCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ('id', 'name', 'is_active', 'date_added', 'updated',)


class CityAreaListSerializer(serializers.ModelSerializer):

    area = AreaInsideCitySerializer(many=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'is_active', 'date_added', 'updated', 'area')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'


"""
class StoreSerializers(serializers.HyperlinkedModelSerializer):

    city = CitySerializer()
    area = AreaSerializer()

    class Meta:
        model = Store
        fields = ('id', 'name', 'city', 'area', 'title_address', 'position', 'opening_time', 'closing_time',
                  'last_order_receiving_time', 'date_added', 'updated', 'is_active',)

"""


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        #fields = '__all__'
        fields = ('id', 'name', 'image', 'width_field', 'height_field', 'city', 'area', 'title_address', 'position', 'opening_time', 'closing_time',
                  'vat_percentage', 'last_order_receiving_time', 'date_added', 'updated', 'is_active',)

