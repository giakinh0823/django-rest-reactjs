from product.models import *
from rest_framework import viewsets
from .pageSerializers import ResultsSetPagination
from .serializers import *
from .filtersSet import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields =["title","category", "service","price" ]
    filter_class = ProductFilter
    ordering_fields = ['price', 'title']



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer



