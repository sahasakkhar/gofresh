from rest_framework import serializers
from products.models import Store, Product, SubCategory, Category, ProductImage


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'image', 'width_field', 'height_field', 'slug', 'created', 'updated', 'is_active')


class CategorySerializer(serializers.ModelSerializer):

    sub_category = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'sub_category', 'name', 'image', 'width_field', 'height_field', 'slug', 'created', 'updated', 'is_active')


class SimpleSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'image', 'width_field', 'height_field', 'slug', 'created', 'updated', 'is_active')


class SimpleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'width_field', 'height_field', 'slug', 'created', 'updated', 'is_active')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'width_field', 'height_field')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = SimpleCategorySerializer()
    sub_category = SimpleSubCategorySerializer()
    images = ProductImageSerializer(many=True)
    

    class Meta:
        model = Product
        fields = ('id', 'category', 'sub_category', 'images', 'name', 'name', 'is_popular', 'description', 'title_price', 'real_price', 'off_percentage',
                  'stock_count', 'vat_percentage', 'created', 'updated', 'is_active',)



