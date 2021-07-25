import django_filters
from product.models import Product
from .serializers import *
from rest_framework import viewsets


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'title': ['exact'],
            'category': ['exact'],
            'service': ['exact'], 
            'size': ['exact'], 
            'price': ['lte', 'gte'],
        }


class ProductList(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_class = ProductFilter
