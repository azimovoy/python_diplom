from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from digitalstore.models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, \
    DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import ProductFilter
from rest_framework.pagination import LimitOffsetPagination


class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListDetailSerializer


class CategoryDetailApiView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListDetailSerializer


class CategoryCreateApiView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CreateEditDeleteCategorySerializer


class CategoryUpdateApiView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CreateEditDeleteCategorySerializer


class CategoryDeleteApiView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CreateEditDeleteCategorySerializer


class ProductPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListDetailSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'brand__title', 'color_name']
    pagination_class = ProductPagination
    ordering = ['price']


class ProductDetailApiView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListDetailSerializer


class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAddChangeDeleteSerializer


class ProductUpdateApiView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAddChangeDeleteSerializer


class ProductDeleteApiView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAddChangeDeleteSerializer


class FavouriteListApiView(ListAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteListDetailSerializer


class UserFavouriteListAPIView(ListAPIView):
    serializer_class = FavouriteListDetailSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return FavouriteProduct.objects.filter(user__id=user_id)


class FavouriteAddApiView(CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteAddDeleteSerializer


class FavouriteDeleteApiView(DestroyAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteAddDeleteSerializer


class FavouriteDetailApiView(RetrieveAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteListDetailSerializer


class OrderListProductApiView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListDetailSerializer


class UserCartListAPIView(ListAPIView):
    serializer_class = OrderListDetailSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return Order.objects.filter(customer=user_id)


class OrderDetailApiView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListDetailSerializer


class OrderAddApiView(CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteAddDeleteSerializer


class OrderDeleteApiView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderAddDeleteSerializer


class OrderProductListApiView(ListAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductListDetailSerializer


class UserOrderAPIView(ListAPIView):
    serializer_class = OrderProductListDetailSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return OrderProduct.objects.filter(order__customer=user_id)


class OrderProductDetailApiView(RetrieveAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductListDetailSerializer


class ShippingAddressApiView(ListAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressListDetailSerializer


class ProfileListApiView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListDetailSerializer


class ProfileDetailApiView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListDetailSerializer


class ProfileUpdateApiView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileAddDeleteSerializer


class ProfileDeleteApiView(DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileAddDeleteSerializer


class UserProfileAPIView(ListAPIView):
    serializer_class = ProfileListDetailSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return Profile.objects.filter(user__id=user_id)
