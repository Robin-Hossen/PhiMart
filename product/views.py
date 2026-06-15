from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product,Category
from product.serializers import ProductSerializer,CategorySerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView


# Create your views here.

# @api_view()
# def view_products(request):
#     product=get_object_or_404(Product,pk=id)
#     serializer=ProductSerializer(product)

#     return Response(serializer.data)


    

class ViewProduct(APIView):
    def get(self,request):    
        products=Product.objects.select_related('category').all()
        serializer=ProductSerializer(products,many=True)#context={'request':request} ata add korte hobe future work
        return Response(serializer.data)
    def post(self,request):
        serializer=ProductSerializer(data=request.data)#deserializer
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class ProductList(ListCreateAPIView):
    queryset=Product.objects.select_related('category').all()
    serializer_class=ProductSerializer
    """needed thing when logical thing needed"""
    # def get_queryset(self):
    #     return Product.objects.select_related('category').all()

    # def get_serializer_class(self):
    #     return ProductSerializer
        


    
# class ViewSpecifiProduct(APIView):
#     def get(self,request,id):
#         product=get_object_or_404(Product,pk=id)
#         serializer=ProductSerializer(product)
#         return Response(serializer.data)
#     def put(self,request,id):
#         product=get_object_or_404(Product,pk=id)
#         serializer=ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     def delete(self,request,id):
#         product=get_object_or_404(Product,pk=id)
#         copy_of_product= product#deleted data dekhar jonne
#         product.delete()
#         serializer=ProductSerializer(copy_of_product)#kon data delete korlm seta dekhanor jonne
#         return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)    

class ProductDetails(RetrieveUpdateDestroyAPIView):# ata dia ViewSpecifiProduct ar kaj hosse matro 2 line dia,
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

class ViewCategories(APIView):
    def get(self,request):
        categories=Category.objects.annotate(product_count=Count('products')).all()
        serializer=CategorySerializer(categories,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class CategoryList(RetrieveUpdateDestroyAPIView):#ata dia ViewCategories kaj hoia jasse 
    queryset=Category.objects.annotate(product_count=Count('products')).all()
    serializer_class=CategorySerializer

class CategoryList(ListCreateAPIView):
    queryset=Category.objects.annotate(product_count=Count('products')).all()
    serializer_class=CategorySerializer






class ViewSpecificCategories(APIView):
    def get(self,request,pk):
        category=get_object_or_404(Category.objects.annotate(product_count=Count('products')),pk=pk)
        serializer=CategorySerializer(category)
        return Response(serializer.data)
    def put(self,request,pk):
        category=get_object_or_404(Category,pk=pk)
        serializer=CategorySerializer(category,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def delete(self,request,pk):
        category=get_object_or_404(Category,pk=pk)
        copy_of_category=category
        category.delete()
        serializer=CategorySerializer(copy_of_category)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

class CategoryDetails(RetrieveUpdateDestroyAPIView):#ata dia ViewSpecificCategories ar kaj hoia gelo
    queryset= Category.objects.annotate(product_count=Count('products')).all()
    serializer_class=CategorySerializer       