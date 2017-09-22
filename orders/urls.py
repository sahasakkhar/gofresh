from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from orders import views as order_view

router = DefaultRouter()
router.register(r'delivery_info', order_view.DeliveryInformationViewSet, 'delivery_info')
router.register(r'orders', order_view.OrderViewSet, 'orders')
router.register(r'products_in_order', order_view.ProductInOrderViewSet, 'products_in_order')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^reset_delivery_cost_form/$', order_view.reset_delivery_cost_form, name='reset_delivery_cost_form'),
    url(r'^reset_delivery_cost/$', order_view.reset_delivery_cost, name='reset_delivery_cost'),
    url(r'^create_order/$', order_view.create_order, name='create_order'),
    ]