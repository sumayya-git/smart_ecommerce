from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from store.models import  Cart, CartItem, Product, Order, OrderItem, Category

from rest_framework import serializers
from store.models import Category

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.StringRelatedField(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    

    def get_image(self, obj):
        if not obj.image:
            return None

        request = self.context.get("request")

        if request:
            url = request.build_absolute_uri(obj.image.url)
            return url.replace("http://", "https://")

        return obj.image.url

    
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            url = request.build_absolute_uri(obj.image.url)
            return url.replace("http://", "https://")
        return None

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = CartItem
        fields = ["id", "product",  "quantity"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items"]




class OrderItemInputSerializer(serializers.Serializer):
     product_id = serializers.IntegerField()
     quantity = serializers.IntegerField()

class OrderCreateSerializer(serializers.Serializer):
      address = serializers.CharField()
      items = OrderItemInputSerializer(many=True)
      payment_method = serializers.CharField(required=False)

      def validate_items(self, value):
          if not value:
              raise serializers.ValidationError("Cart is empty")
          return value
      
      def validate_address(self, value):
          if len(value.strip()) < 5:
              raise serializers.ValidationError("Address too short")
          
          return value
      


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"



class MyTokenSerializer(TokenObtainPairSerializer): 
      def validate(self, attrs):
          data = super().validate(attrs)

          data["username"] = self.user.username
          data["role"] = "admin" if self.user.is_staff else "user"

          return data
     








# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from .serializers import CartSerializer

# class CartDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#       cart, _ = Cart.objects.get_or_create(user=request.user)
#       serializer = CartSerializer(cart)
#       return Response(serializer.data)
    

# class AddToCartAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#       product_id = request.data.get("product_id")
#       product = Product.objects.get(id=product_id)
#       cart,_ = Cart.objects.get_or_create(user=request.user)

#       item, created = CartItem.objects.get_or_create(cart=cart, product=product)

#       if not created:
#           item.quantity += 1
#           item.save()
        
#       return Response({"message": "Item added to cart"})
    

# class RemoveFromCartAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, item_id):
#       CartItem.objects.filter(
#           id=item_id,
#           cart__user=request.user).delete()
#       return Response({"message": "Item removed"})
      


    

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ["id", "name", "slug"]


# class ProductSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
    
#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "name",
#             "price",
#             "description",
#             "image",
#             "category",
#         ]



  


# class OrderCreateSerializer(serializers.Serializer):
#     items = OrderItemSerializer(many=True)
#     address = serializers.CharField()

#     def create(self, validated_data):
#         request = self.context["request"]
       
        
#         order= Order.objects.create(
#             user=request.user,
#             address=validated_data['address'],
#             total_amount=0,
#             status='PLACED'
#         )

#         total= 0

#         for item in validated_data["items"]:
#             product=Product.objects.get(id=item["product_id"])
#             qty = item["quantity"]
#             price = product.price * qty

#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=qty,
#                 price=price
#             )

#             total += price
#         order.total_amount = total
#         order.save()
        

#         return order
    

# class OrderItemListSerializer(serializers.ModelSerializer):
#     product = serializers.CharField(source="product.name")

#     class Meta:
#         model = OrderItem
#         fields = ["product", "quantity", "price"]


    
# class OrderListSerializer(serializers.ModelSerializer):
#      items = OrderItemListSerializer(many=True)

#      class Meta:
#         model = Order
#         fields = ["id","total_amount", "status", "created_at", "items"]


     
    






    
    


   