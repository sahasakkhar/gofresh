from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import Product, Category, SubCategory, ProductImage


class SubCategoryInline(admin.TabularInline):

    model = SubCategory
    show_change_link = True
    extra = 4
    ordering = ['created']


class CategoryAdmin(admin.ModelAdmin):

    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['created', 'is_active', 'updated']
    readonly_fields = ['id', 'created', 'updated', ]
    list_display_links = ['name',]
    ordering = ['created',]

    inlines = [SubCategoryInline,]


class SubCategoryAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'category']
    search_fields = ['id', 'name',]
    list_filter = ['category', 'created', 'is_active', 'updated']
    readonly_fields = ['id', 'created', 'updated', ]
    list_display_links = ['name']
    ordering = ['created',]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ('render_image', 'image', 'width_field', 'height_field')
    readonly_fields = ('render_image',)
    extra = 5

    def render_image(self, obj):
        return mark_safe('<img src="%s" width="100" height="150" />' % (obj.image.url))

    render_image.short_description = 'Image Preview'


class ProductAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'is_popular', 'category', 'sub_category', 'store',]
    search_fields = ['id', 'name',]
    list_filter = ['category', 'is_popular', 'sub_category', 'created', 'is_active', 'updated']
    readonly_fields = ['id', 'created', 'updated', ]
    list_display_links = ['name']
    ordering = ['created',]
    inlines = [ProductImageInline, ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
