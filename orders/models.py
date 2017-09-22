from datetime import date

from django.utils.safestring import mark_safe

from accounts.models import UserProfile
from customutils.full_scope_static import MAX_CHAR_LENGTH, DELIVERY_TIME_SLOTS, TIME_SLOT_1, \
    DELIVERY_STATUS, PENDING, MAX_INVOICE_NUMBER_LENGTH, SMALL_CHAR_LENGTH
from customutils.method_box import generate_invoice_number, get_delivery_cost
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product, ProductImage
from smart_selects.db_fields import ChainedForeignKey
from stores.models import Store


class DeliveryInformation(models.Model):

    phone_regex = RegexValidator(regex=r'^\+?\(?\d{2,4}\)?[\d\s-]{3,15}$',
                                 message="Phone number must be entered in the format: '+999999999' '+880155456509'. Up to 15 digits allowed.")
    user_profile = models.ForeignKey(UserProfile)
    area = models.CharField(max_length=MAX_CHAR_LENGTH, blank=False)
    road_no = models.CharField(max_length=MAX_CHAR_LENGTH, blank=True)
    house_no = models.CharField(max_length=MAX_CHAR_LENGTH, blank=True)
    floor_no = models.CharField(max_length=MAX_CHAR_LENGTH, blank=True)
    address_detail = models.CharField(max_length=MAX_CHAR_LENGTH, blank=True)

    product_receiver_name = models.CharField(max_length=MAX_CHAR_LENGTH, blank=False)
    product_receiver_phone = models.CharField(validators=[phone_regex], blank=False, max_length=15) # validators should be a list
    product_receiver_phone_optional = models.CharField(validators=[phone_regex], blank=True, max_length=15)

    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Order(models.Model):

    user_profile = models.ForeignKey(UserProfile, related_name='order_user_profile')
    store = models.ForeignKey(Store, related_name='orders', default=None)
    delivery_information = models.ForeignKey(DeliveryInformation, related_name='order_delivery_information')

    delivery_status = models.IntegerField(choices=DELIVERY_STATUS, default=PENDING)
    invoice_number = models.CharField(max_length=MAX_INVOICE_NUMBER_LENGTH, blank=True)

    delivery_date = models.DateField(default=date.today, blank=False)
    delivery_time = models.IntegerField(choices=DELIVERY_TIME_SLOTS, default=TIME_SLOT_1, blank=False)

    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def total_expense(self):
        
        product_list = ProductInOrder.objects.filter(order=self.id)
        total_price = 0
        for each in product_list:
            total_price += (each.product.real_price*each.quantity)
        return str(total_price+get_delivery_cost())

    total_expense.allow_tags = True

    def __str__(self):
        return str(self.invoice_number)


class ProductInOrder(models.Model):

    order = models.ForeignKey(Order, related_name='products')
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(blank=False, default=1)

    class Meta:
        unique_together = ['order', 'product']

    def __str__(self):
        return str(self.order.id)


@receiver(post_save, sender=Order)
def post_save_auth_user(signal, sender, instance, **kwargs):
    if kwargs.get('created') is True:
        instance.invoice_number = generate_invoice_number()
        instance.save()

