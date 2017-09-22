from django.db.models import Q
import copy
from django_filters.rest_framework import DjangoFilterBackend

from customutils.custom_authentication import AppTokenAuthentication
from django.contrib.postgres.search import SearchVector

from customutils.method_box import get_delivery_cost
from products.models import Product, Category, ProductImage
from products.serializers import ProductSerializer, SimpleCategorySerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from stores.models import Store


class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (AppTokenAuthentication,)

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('store', 'category', 'sub_category', 'is_popular')


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def product_search(request):

    query = request.GET.get('query')
    store = request.GET.get('store')
    products = Product.objects.annotate(search=SearchVector('name') + SearchVector('description')).filter(search=query, store=store)

    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def products_for_home(request):
    store_id = request.GET.get('store_id')
    store = Store.objects.get(id=store_id)
    print(store_id)
    data = {}
    category_list = []
    product_list = []

    categories = Category.objects.all()
    for category in categories:
        products = Product.objects.filter(Q(store=store) & Q(category=category) & Q(is_popular=True)).order_by('name')[:5]
        if len(products) > 0:
            category_list.append(category)
            for each in products:
                product_list.append(each)

    serializer = ProductSerializer(product_list, many=True, context={"request": request})
    data['products'] = serializer.data

    serializer_category = SimpleCategorySerializer(category_list, many=True, context={"request": request})
    data['categories'] = serializer_category.data

    popular_list = Product.objects.filter(Q(store=store) & Q(is_popular=True)).order_by('name')[:5]
    popular_serializer = ProductSerializer(popular_list, many=True, context={"request": request})
    data['popular'] = popular_serializer.data
    data['delivery_cost'] = get_delivery_cost()

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def copy_products(request):

    from_store_id = request.GET.get('from_store_id')
    to_store_id = request.GET.get('to_store_id')

    try:
        from_store = Store.objects.get(id=from_store_id)
        to_store = Store.objects.get(id=to_store_id)

        product_list = Product.objects.filter(store=from_store)
        for product in product_list:
            new_product = copy.deepcopy(product)

            new_product.id = None
            new_product.store = to_store
            new_product.save()

            product_images = ProductImage.objects.filter(product=product)
            for product_image in product_images:
                new_product_image = copy.deepcopy(product_image)
                new_product_image.id = None
                new_product_image.product = new_product
                new_product_image.save()

        return Response(data={'msg': 'ok'}, status=status.HTTP_200_OK)

    except Store.DoesNotExist:
        return Response(data={'msg': 'store not found'}, status=status.HTTP_200_OK)

