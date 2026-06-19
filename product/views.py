
from rest_framework.response import Response
from rest_framework import status
from product.models import Product,Category,Review,ProductImage
from product.serializers import ProductSerializer,CategorySerializer,ReviewSerializer,ProductImageSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from product.pagination import DefaultPagination
from api.permissions import IsAdminOrReadOnly,FullDjangoModelPermission
from rest_framework.permissions import DjangoModelPermissions
from product.permissions import IsReviewAuthorOrReadonly

class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store
    - Allows authenticated admin to create,update and delete producs
    - Allows users to brpws and filter product
    - Support searching by name, description and category
    - Support ordering by price and updated_at
    """
    queryset=Product.objects.all()#all product dekhai
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    pagination_class=DefaultPagination
    search_fields=['name','description','category__name']
    ordering_fields=['price']
    permission_classes=[IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        """Retive all products"""
        return super().list(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        """ only Authenticated Admin can create product"""
        return super().create(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]

    queryset=Category.objects.annotate(product_count=Count('products')).all()
    serializer_class=CategorySerializer



class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    permission_classes=[IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)    

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])#specific dekhar jonne

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}


class ProductImageViewset(ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]
    serializer_class=ProductImageSerializer
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])#specific dekhar jonne
    
    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['product_pk'])
