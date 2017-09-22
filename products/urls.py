from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from products import views as product_view

router = DefaultRouter()
router.register(r'products', product_view.ProductViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^product_search/$', product_view.product_search, name='product_search'),
    url(r'^products_for_home/$', product_view.products_for_home, name='products_for_home'),
    url(r'^copy_products/$', product_view.copy_products, name='copy_products'),
]