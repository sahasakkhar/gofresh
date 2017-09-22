import datetime
from django.db import models
from customutils.full_scope_static import MAX_CHAR_LENGTH, DEFAULT_LAST_ORDER_RECEIVING_TIME, DEFAULT_STORE_OPENING_TIME, DEFAULT_STORE_CLOSING_TIME, TIME_CHOICES, \
    SMALL_CHAR_LENGTH
from smart_selects.db_fields import GroupedForeignKey, ChainedForeignKey
from geoposition.fields import GeopositionField


class City(models.Model):

    name = models.CharField(max_length=SMALL_CHAR_LENGTH, blank=False)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ('-date_added',)

    def __str__(self):
        return self.name


class Area(models.Model):
    city = models.ForeignKey(City, related_name='area', null=True)
    name = models.CharField(max_length=SMALL_CHAR_LENGTH, blank=False)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ('-date_added',)

    def __str__(self):
        return self.name


def store_upload_location(instance, filename):
    return "store/%s" % filename


class Store(models.Model):

    city = models.ForeignKey(City, related_name='store_city', null=True)

    area = ChainedForeignKey(
        Area,
        chained_field="city",
        chained_model_field="city",
        show_all=False,
        auto_choose=True,
        related_name='store_area',
        null=True
    )

    name = models.CharField(max_length=SMALL_CHAR_LENGTH, blank=False)

    image = models.ImageField(null=True,
                              blank=True,
                              default='store/default.png',
                              upload_to=store_upload_location,
                              width_field='width_field',
                              height_field='height_field')

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    title_address = models.CharField(max_length=MAX_CHAR_LENGTH, blank=True)
    position = GeopositionField()
    opening_time = models.TimeField(choices=TIME_CHOICES, default=DEFAULT_STORE_OPENING_TIME)
    closing_time = models.TimeField(choices=TIME_CHOICES, default=DEFAULT_STORE_CLOSING_TIME)
    last_order_receiving_time = models.TimeField(choices=TIME_CHOICES, default=DEFAULT_LAST_ORDER_RECEIVING_TIME)
    vat_percentage = models.FloatField(default=0, blank=False)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

