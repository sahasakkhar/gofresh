from django.db import models
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe

from customutils.full_scope_static import MAX_CHAR_LENGTH
from stores.models import Store
from smart_selects.db_fields import GroupedForeignKey, ChainedForeignKey


def category_upload_location(instance, filename):
    return "category/%s" % filename


class Category(models.Model):

    #store = models.ForeignKey(Store, related_name='store', blank=True, null=True)
    name = models.CharField(max_length=MAX_CHAR_LENGTH, blank=False)

    image = models.ImageField(null=True,
                              blank=True,
                              default='category/default.png',
                              upload_to=category_upload_location,
                              width_field='width_field',
                              height_field='height_field')

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    slug = models.SlugField(blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta(object):
        ordering = ('-created',)

    def __str__(self):
        return self.name


def sub_category_upload_location(instance, filename):
    return "sub_category/%s" % filename


class SubCategory(models.Model):

    category = models.ForeignKey(Category, related_name='sub_category')
    name = models.CharField(max_length=MAX_CHAR_LENGTH, blank=False)
    image = models.ImageField(null=True,
                              blank=True,
                              default='sub_category/default.png',
                              upload_to=sub_category_upload_location,
                              width_field='width_field',
                              height_field='height_field')

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    slug = models.SlugField(blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):

    store = models.ForeignKey(Store, related_name='store')
    category = models.ForeignKey(Category, related_name='product_category', null=True)

    sub_category = ChainedForeignKey(
        SubCategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        related_name='product_sub_category',
        null=True
    )


    name = models.CharField(max_length=MAX_CHAR_LENGTH, blank=False)

    slug = models.SlugField(blank=True)
    description = models.TextField()
    title_price = models.CharField(max_length=MAX_CHAR_LENGTH, blank=False)
    real_price = models.PositiveIntegerField(default=0, blank=False)
    stock_count = models.PositiveIntegerField(default=100, blank=False)
    off_percentage = models.PositiveIntegerField(default=0, blank=False)
    vat_percentage = models.FloatField(default=0, blank=False)

    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta(object):
        ordering = ('name',)

    def __str__(self):
        return self.name


def upload_location(instance, filename):
    return "product/%s/%s" % (instance.product.id, filename)


class ProductImage(models.Model):

    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(null=True,
                              blank=True,
                              default='product/default.png',
                              upload_to=upload_location,
                              width_field = 'width_field',
                              height_field = 'height_field')

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
