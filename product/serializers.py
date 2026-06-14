from rest_framework import serializers
from decimal import Decimal #type casting ar jonne
from product.models import Category


class CategorySerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    description=serializers.CharField()



class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    price=serializers.DecimalField(max_digits=10, decimal_places=2)

    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    
    #there are 4 way to show category

        
    # 1.category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # 2.category=serializers.StringRelatedField()
    # 3.category=CategorySerializer()
    category=serializers.HyperlinkedRelatedField(queryset=Category.objects.all(),view_name='view_specific_category')

    def calculate_tax(self,product):
        return round(product.price*Decimal(1.1),2)#type casting