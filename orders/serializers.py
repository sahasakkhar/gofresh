from accounts.serializers import UserProfileSerializer
from orders.models import DeliveryInformation, Order, ProductInOrder
from products.serializers import ProductSerializer
from rest_framework import serializers


class DeliveryInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryInformation
        fields = '__all__'


class OrderDeliveryInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryInformation
        exclude = ('user_profile',)


class ProductInOrderSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = ProductInOrder
        fields = ('product', 'quantity', 'id', 'order')


class CustomProductInOrderSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):

    delivery_information = DeliveryInformationSerializer()
    products = ProductInOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id','user_profile', 'delivery_information', 'products', 'total_expense', 'delivery_status',
                  'delivery_time', 'delivery_date', 'invoice_number', 'date_added', 'updated', )


"""
class OrderSerializerCreate(serializers.ModelSerializer):

    products = CustomProductInOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user_profile', 'delivery_information', 'products', 'delivery_time', 'delivery_date',)


    def create(self, validated_data):
        print(validated_data)
        products_in_order = validated_data.pop('products')

        order = Order.objects.create(**validated_data)
        for product in products_in_order:
            ProductInOrder.objects.create(order=order, **product)
        return order
"""



