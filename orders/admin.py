from django.shortcuts import redirect
from django.template import RequestContext
from weasyprint import HTML, CSS

from accounts.models import UserProfile
from customutils.full_scope_static import DELIVERY_TIME_SLOTS
from customutils.method_box import get_delivery_cost
from orders.views import reset_delivery_cost_form

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django_object_actions import DjangoObjectActions
from html import escape
from os.path import join
from gofresh import settings
from orders.models import Order, DeliveryInformation, ProductInOrder
from products.models import ProductImage



class DeliveryInformationAdmin(admin.ModelAdmin):

    list_display = ['id', 'user_profile', 'area']
    search_fields = ['id', 'user_profile__auth_user__email',]
    list_filter = ['user_profile', 'date_added', 'updated']
    readonly_fields = ['id', 'date_added', 'updated', ]
    list_display_links = ['id']
    ordering = ['-date_added',]


class ProductImageInline(admin.TabularInline):

    model = ProductImage
    fields = ('render_image', 'image', 'width_field', 'height_field')
    readonly_fields = ('render_image',)
    extra = 5

    def render_image(self, obj):
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.image.url))

    render_image.short_description = 'Image Preview'


class ProductInOrderInline(admin.TabularInline):

    model = ProductInOrder
    fields = ('thumb', 'product_name', 'product_title_price', 'product_real_price', 'product_off_percentage', 'order', 'quantity')
    readonly_fields = ('thumb', 'product_title_price', 'product_real_price', 'quantity', 'product_name', 'product_off_percentage')
    extra = 0

    def thumb(self, obj):
        images = ProductImage.objects.filter(product=obj.product)
        return mark_safe('<img src="%s" width="150" height="150" />' % (images[0].image.url))

    thumb.short_description = 'Thumb'

    def product_title_price(self, obj):
        return obj.product.title_price

    product_title_price.short_description = 'Title Price'

    def product_real_price(self, obj):
        return obj.product.real_price

    product_real_price.short_description = 'Real Price'

    def product_off_percentage(self, obj):
        return obj.product.off_percentage

    product_off_percentage.short_description = 'Off Percentage'


    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = 'Title'


class OrderAdmin(DjangoObjectActions, admin.ModelAdmin):

    list_display = ['id', 'invoice_number', 'store', 'delivery_status', 'total_expense', 'delivery_date', 'delivery_time', 'date_added']
    search_fields = ['id', 'user_profile__auth_user__email', 'invoice_number']
    list_filter = ['user_profile', 'delivery_status', 'delivery_date', 'delivery_time', 'date_added',]

    readonly_fields = ['id', 'date_added', 'updated', 'delivery_area', 'delivery_road_no', 'delivery_road_no',
                       'delivery_house_no', 'delivery_floor_no', 'delivery_address_detail',
                       'delivery_product_receiver_name', 'delivery_product_receiver_phone',
                       'delivery_product_receiver_phone_optional', 'name', 'email', 'total_expense',
                       'store_address', 'delivery_date', 'delivery_time', 'invoice_number']
    list_display_links = ['id', 'invoice_number', 'store']
    ordering = ['-date_added',]

    fieldsets = [
        ('Invoice', {'fields' : ['invoice_number']}),
        ('Store', {'fields': ['store_address']}),
        ('Order Creator', {'fields': ['name', 'email']}),

        ('Delivery Information', {'fields': ['delivery_area', 'delivery_road_no',
                       'delivery_house_no', 'delivery_floor_no', 'delivery_address_detail',
                       'delivery_product_receiver_name', 'delivery_product_receiver_phone', 'delivery_product_receiver_phone_optional']}),

        ('Delivery Status', {'fields': ['delivery_status']}),
        ('Total Expense', {'fields': ['total_expense']}),
        ('Date', {'fields': ['delivery_date', 'delivery_time', 'date_added']}),
    ]

    inlines = [ProductInOrderInline, ]

    def store_address(self, obj):
        store_info = '%s\n%s\n%s\n%s' % (obj.store.name, obj.store.title_address, obj.store.area, obj.store.city)
        return store_info

    def name(self, obj):
        return obj.user_profile.name

    def email(self, obj):
        return obj.user_profile.auth_user.email

    def delivery_area(self, obj):
        return obj.delivery_information.area

    def delivery_road_no(self, obj):
        return obj.delivery_information.road_no

    def delivery_house_no(self, obj):
        return obj.delivery_information.house_no

    def delivery_floor_no(self, obj):
        return obj.delivery_information.floor_no

    def delivery_address_detail(self, obj):
        return obj.delivery_information.address_detail

    def delivery_product_receiver_name(self, obj):
        return obj.delivery_information.product_receiver_name

    def delivery_product_receiver_phone(self, obj):
        return obj.delivery_information.product_receiver_phone

    def delivery_product_receiver_phone_optional(self, obj):
        return obj.delivery_information.product_receiver_phone_optional

    def change_delivery_cost(self, request, obj):
        return redirect('/reset_delivery_cost_form/')

    def generate_invoice(self, request, obj):

        html_template = get_template('orders/invoice_generator.html')
        products_in_order = ProductInOrder.objects.filter(order=obj)
        total_price = 0
        vat = 0
        for each in products_in_order:
            total_price = total_price + (each.product.real_price*each.quantity)

            if each.product.vat_percentage > 0:
                vat_per_product = (each.product.real_price*each.product.vat_percentage)/100
                vat = vat + (vat_per_product*each.quantity)
            elif each.product.store.vat_percentage > 0 :
                vat_per_product = (each.product.real_price * each.product.store.vat_percentage) / 100
                vat = vat + (vat_per_product * each.quantity)

        total_price = total_price+vat+get_delivery_cost()
        context = {'order': obj, 'delivery_time_slot': DELIVERY_TIME_SLOTS[obj.delivery_time-1][1], 'vat':vat,
                   'total_price': total_price, 'products_in_order': products_in_order, 'delivery_cost': get_delivery_cost()}

        rendered_html = html_template.render(context).encode(encoding="UTF-8")

        pdf_file = HTML(string=rendered_html).write_pdf()

        http_response = HttpResponse(pdf_file, content_type='application/pdf')

        pdf_name = obj.user_profile.auth_user.email+'_'+obj.invoice_number+'.pdf'
        http_response['Content-Disposition'] = 'filename='+pdf_name
        return http_response

    generate_invoice.label = "Generate Invoice"  # optional
    change_delivery_cost.label = 'Change Delivery Cost'
    generate_invoice.short_description = "pdf generator and print"  # optional
    change_actions = ('generate_invoice', 'change_delivery_cost')


class ProductInOrderAdmin(admin.ModelAdmin):

    list_display = ['id', 'product', 'order',]
    search_fields = ['id', 'order__user_profile__auth_user__email', 'order__invoice_number']
    list_filter = ['order']
    readonly_fields = ['id']
    list_display_links = ['id', 'product']
    ordering = ['-order__date_added',]


admin.site.register(DeliveryInformation, DeliveryInformationAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
