from django_filters import rest_framework as filters
from digitalstore.models import Product


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    category = filters.CharFilter(field_name="category__title", lookup_expr='icontains')
    brand = CharFilterInFilter(field_name='brand__title', lookup_expr='in')
    color_name = CharFilterInFilter(field_name='color_name', lookup_expr='in')
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['brand', 'color_name', 'price', 'title', 'category']
