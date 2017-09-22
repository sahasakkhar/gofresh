from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from stores import views as store_view

router = DefaultRouter()
router.register(r'stores', store_view.StoreViewSet)
router.register(r'city', store_view.CityViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^find_store_with_location/$', store_view.find_store_with_location, name='find_store_with_location'),
    url(r'^find_store/$', store_view.find_store, name='find_store'),
    ]