from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


@api_view(['GET'])
def cart_detail_api(request):
    cart = request.session.get('cart',{})
    items = []

    for pid, qty in cart.items():

        product = Product.objects.get(id=int(pid))
        items.append({
            "product": product.name,
            "quantity": qty
        })
   
    return Response({"id":1,"items": items })


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)