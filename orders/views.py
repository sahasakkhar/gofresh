from django.core.cache import cache

from accounts.models import UserProfile
from customutils.custom_authentication import AppTokenAuthentication
from django.shortcuts import render, get_object_or_404
from orders.models import DeliveryInformation, Order, ProductInOrder
from orders.serializers import DeliveryInformationSerializer, ProductInOrderSerializer, CustomProductInOrderSerializer, \
    OrderSerializer
from products.models import Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from django.utils.six import BytesIO

from stores.models import Store


class DeliveryInformationViewSet(viewsets.ModelViewSet):

    queryset = DeliveryInformation.objects.all()
    serializer_class = DeliveryInformationSerializer
    #authentication_classes = (AppTokenAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user_profile',)


class OrderViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):

        if self.action == 'list':
            return OrderSerializer

        elif self.action == 'retrieve':
            return OrderSerializer

        elif self.action == 'create':
            print("get_serializer_class : " + "create")
            return OrderSerializer

        return OrderSerializer

    queryset = Order.objects.all()
    filter_fields = ('user_profile',)
    #permission_classes = (AllowAny,)
    serializer_class = get_serializer_class
    #authentication_classes = (AppTokenAuthentication,)
    filter_backends = (DjangoFilterBackend,)


class ProductInOrderViewSet(viewsets.ModelViewSet):

    queryset = ProductInOrder.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductInOrderSerializer
    #authentication_classes = (AppTokenAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('order', 'order__invoice_number')


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
#@authentication_classes((AppTokenAuthentication,))
def create_order(request):

    user_profile = UserProfile.objects.get(id=request.POST.get('user_profile'))
    delivery_information = request.POST.get('delivery_information')
    delivery_date = request.POST.get('delivery_date')
    delivery_time = request.POST.get('delivery_time')
    products = request.POST.get('products')
    store_id = request.data['store_id']

    delivery_information_instance = DeliveryInformation.objects.get(id=delivery_information)
    store = Store.objects.get(id = store_id)
    order = Order.objects.create(user_profile=user_profile, delivery_information=delivery_information_instance, store= store,
                                 delivery_date=delivery_date, delivery_time=delivery_time)

    stream = BytesIO(products.encode())
    products_data = JSONParser().parse(stream)

    products_serializer = CustomProductInOrderSerializer(data=products_data, many=True)

    if products_serializer.is_valid():
        for each in products_serializer.data:
            each_product_in_order = (dict(each))
            each_product_id_in_order = Product.objects.get(id=each_product_in_order['product'])
            ProductInOrder.objects.create(order=order, product=each_product_id_in_order,
                                          quantity=each_product_in_order['quantity'])

        data = dict()
        data['invoice_number'] = order.invoice_number
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        return Response(data=products_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
def reset_delivery_cost_form(request):
    return Response(status=status.HTTP_200_OK, template_name='orders/delivery_cost_reset_form.html')


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def reset_delivery_cost(request):
    delivery_cost = request.POST.get('delivery_cost')
    cache.set('delivery_cost', delivery_cost, None)

    '''
    fo = open('delivery_cost.txt', 'w')
    fo.write(str(delivery_cost))
    fo.close()

    '''


    data = {'message': 'Changed'}
    return Response(data=data, status=status.HTTP_200_OK)