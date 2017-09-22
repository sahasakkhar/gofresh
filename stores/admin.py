from django.contrib import admin
from products.models import Product
from stores.models import City, Area, Store


class AreaInline(admin.TabularInline):

    model = Area
    show_change_link = True
    extra = 4
    ordering = ['date_added']


class CityAdmin(admin.ModelAdmin):

    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['date_added', 'is_active', 'updated']
    readonly_fields = ['id', 'date_added', 'updated', ]
    list_display_links = ['name',]
    ordering = ['date_added',]

    inlines = [AreaInline,]


class StoreInline(admin.TabularInline):

    model = Store
    show_change_link = True
    extra = 4
    ordering = ['date_added']


class AreaAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'city']
    search_fields = ['id', 'name',]
    list_filter = ['city', 'date_added', 'is_active', 'updated']
    readonly_fields = ['id', 'date_added', 'updated', ]
    list_display_links = ['name']
    ordering = ['date_added',]

    inlines = [StoreInline,]


class ProductInline(admin.StackedInline):

    model = Product
    show_change_link = True
    extra = 4
    ordering = ['created']


class StoreAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'city', 'area', 'title_address',]
    search_fields = ['id', 'name',]
    list_filter = ['city', 'area', 'date_added', 'is_active', 'updated']
    readonly_fields = ['id', 'date_added', 'updated', ]
    list_display_links = ['name']
    ordering = ['date_added',]

    inlines = [ProductInline, ]

admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Store, StoreAdmin)
