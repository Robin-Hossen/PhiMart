from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product,Category
from product.serializers import ProductSerializer,CategorySerializer
from django.db.models import Count
from rest_framework.views import APIView


# Create your views here.

# @api_view()
# def view_products(request):
#     product=get_object_or_404(Product,pk=id)
#     serializer=ProductSerializer(product)

#     return Response(serializer.data)

@api_view(['GET','POST'])
def view_products(request):
    if request.method=='GET':
        products=Product.objects.select_related('category').all()
        serializer=ProductSerializer(products,many=True)#context={'request':request} ata add korte hobe future work
        return Response(serializer.data)
    if request.method=='POST':
        serializer=ProductSerializer(data=request.data)#deserializer
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    

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
    
           

@api_view(['GET','PUT','DELETE'])
def view_specific_product(request,id):
    if request.method=='GET':
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    if request.method=='PUT':
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    if request.method=='DELETE':
        product=get_object_or_404(Product,pk=id)
        copy_of_product= product#deleted data dekhar jonne
        product.delete()
        serializer=ProductSerializer(copy_of_product)#kon data delete korlm seta dekhanor jonne
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
    
class ViewSpecifiProduct(APIView):
    def get(self,request,id):
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    def put(self,request,id):
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request,id):
        product=get_object_or_404(Product,pk=id)
        copy_of_product= product#deleted data dekhar jonne
        product.delete()
        serializer=ProductSerializer(copy_of_product)#kon data delete korlm seta dekhanor jonne
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)    

@api_view()
def view_categories(request):
    categories=Category.objects.annotate(product_count=Count('products')).all()
    serializer=CategorySerializer(categories,many=True)
    return Response(serializer.data)

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


@api_view()
def view_specific_categories(request,pk):
    category=get_object_or_404(Category,pk=pk)
    serializer=CategorySerializer(category)
    return Response(serializer.data)



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

        