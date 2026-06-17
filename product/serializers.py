from rest_framework import serializers
from decimal import Decimal #type casting ar jonne
from product.models import Category,Product,Review
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    product_count=serializers.IntegerField(read_only=True)#read_only means get ar time a data dau post ar time a no need
    class Meta:
        model=Category
        fields=['id','name','description','product_count']

        




# class ProductSerializer(serializers.Serializer):
#     id=serializers.IntegerField()
#     name=serializers.CharField()
#     price=serializers.DecimalField(max_digits=10, decimal_places=2)

#     price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    
#     #there are 4 way to show category

        
#     # 1.category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     # 2.category=serializers.StringRelatedField()
#     # 3.category=CategorySerializer()
#     category=serializers.HyperlinkedRelatedField(queryset=Category.objects.all(),view_name='view_specific_category')

#     def calculate_tax(self,product):
#         return round(product.price*Decimal(1.1),2)#type casting


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields=['id','name','description','price','category','stock','price_with_tax']

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
        
