from rest_framework import serializers
from .models import Product, Order, OrderItem, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
     
     product_name = serializers.CharField(source="product.name", read_only=True)
     class Meta:
        model = OrderItem
        fields = ["id", "product_name",  "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
     items = OrderItemSerializer(many=True, read_only=True)
     class Meta:
        model = Order
        fields = "__all__"
        
        

class OrderItemInputSerializer(serializers.Serializer):
    product_id =serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    address =serializers.CharField()
    items = OrderItemInputSerializer(many=True)


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    price= serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id","product","product_name","price","image","quantity"]

   