"""gofresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from full_scope_api import api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^', include('accounts.urls', namespace='accounts')),
    url(r'^', include('stores.urls', namespace='stores')),
    url(r'^', include('orders.urls', namespace='orders')),
    url(r'^', include('products.urls', namespace='products')),
    url(r'^full_scope_api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_initial_information/$', api.get_initial_information, name='get_initial_information'),
]
