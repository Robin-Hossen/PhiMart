from rest_framework import serializers
from decimal import Decimal #type casting ar jonne
from product.models import Category,Product,Review,ProductImage
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    product_count=serializers.IntegerField(read_only=True)#read_only means get ar time a data dau post ar time a no need
    class Meta:
        model=Category
        fields=['id','name','description','product_count']

        

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id','image']


class ProductSerializer(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True,read_only=True)#onek image thakte pare and image nau dte pari
    class Meta:
        model= Product
        fields=['id','name','description','price','category','stock','price_with_tax','images']

    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    # category=serializers.HyperlinkedRelatedField(queryset=Category.objects.all(),view_name='view_specific_category')

    def calculate_tax(self,product):
        return round(product.price*Decimal(1.1),2)
    
    def validate_price(self,price):
        if price<0:
            raise serializers.ValidationError("price can't be negetive")
        return price
        






class SimpleUserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(method_name='get_current_user_name')


    class Meta:
        model=get_user_model()
        fields=['id','name']
    
    def get_current_user(self,obj):
        return obj.get_full_name()


class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model=Review
        fields=['id','user','product','ratings','comment']
        read_only_fields=['user','product']

    def get_user(self,obj):
        return SimpleUserSerializer(obj.user).data   

    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)  
        
