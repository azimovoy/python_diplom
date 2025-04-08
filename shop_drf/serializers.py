from rest_framework import serializers
from digitalstore.models import *


class CategoryListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CreateEditDeleteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'icon')


class ProductListDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField('title', read_only=True)
    brand = serializers.SlugRelatedField('title', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductAddChangeDeleteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='title')
    brand = serializers.SlugRelatedField(queryset=BrandProduct.objects.all(), slug_field='title')

    class Meta:
        model = Product
        exclude = ('id', 'slug', 'created_at')


class FavouriteListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteProduct
        fields = '__all__'


class FavouriteAddDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteProduct
        exclude = ('id',)


class OrderListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderAddDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('id', 'created_at', 'is_completed', 'payment', 'shopping')

    def create(self, validated_data):
        validated_data['is_completed'] = False
        validated_data['payment'] = False
        validated_data['shopping'] = False
        return super().create(validated_data)


class OrderProductListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'


class ShippingAddressListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class ProfileListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileAddDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('id',)

