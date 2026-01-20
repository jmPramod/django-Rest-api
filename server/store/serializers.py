from rest_framework import serializers
from .models import ProductModel, CategoryModel,CartItemModels,CartModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ProductModel   # ✅ FIX HERE
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name',read_only=True)
    product_price=serializers.DecimalField(source='product.price',max_digits=10,decimal_places=2,read_only=True)
    product_image=serializers.ImageField(source='product.image' ,read_only=True)
    class Meta:
        model=CartItemModels
        fields='__all__'
        
class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True) 
    total=serializers.ReadOnlyField()
    
    class Meta:
        model=CartModel
        fields='__all__'