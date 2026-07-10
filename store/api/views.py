import razorpay
import socket 
socket.setdefaulttimeout(30)
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics 
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer
from store.models import  Product
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from store.models import Cart, CartItem, Order, OrderItem
from store.serializers import OrderSerializer
from store.serializers import OrderCreateSerializer
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
import csv
from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image, HRFlowable, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import io
import os
from decimal import Decimal
import qrcode
from reportlab.platypus import Image
import hashlib
from reportlab.lib.colors import lightgrey
import base64
from django.db.models import Q
from store.models import UserProfile
from django.db import transaction
from store.utils import send_invoice_email


from rest_framework.decorators import api_view
from store.models import Category
from .serializers import CategorySerializer
from django.contrib.auth import authenticate, login, logout


from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from.utils import success_response, error_response

from django_ratelimit.decorators import ratelimit # fixed


from django.middleware.csrf import get_token

from .logging import log_info, log_warning, log_error


from django.http import JsonResponse
from .tasks import test_task

from .tasks import send_order_email, send_invoice_email_task

from .resend import send_resend_email

from django.core.cache import cache



from django.views.decorators.cache import cache_page





def celery_test(request):
    test_task.delay()
    return JsonResponse({"message": "Task sent to Celery"})



def csrf_failure(request, reason=""):
     

        
        print("-" * 60)
        print("CSRF FAILURE")
        print("REASON:", reason)
       
        print("COOKIE:", request.COOKIES)
       
        print("HEADER:", request.META.get("HTTP_X_CSRFTOKEN"))
        print("=" * 60)



        return JsonResponse(
            {
                "error": "CSRF Failed",
                "reason": reason,
            },
            status=403,
        )








@ensure_csrf_cookie
def csrf(request):
    print("CSRF VIEW HIT")
    token = get_token(request)

    return JsonResponse({"csrftoken": token})

    
# @method_decorator(ensure_csrf_cookie, name='dispatch')

# @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='post')
class LoginView(APIView):
   
    permission_classes = [AllowAny]

    
    def post(self, request):
        
        print("LOGIN VIEW ENTERED")
    
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
           print("BEFORE LOGIN TOKEN:", get_token(request))
           login(request, user)

          

           log_info(f"User {user.username} logged in.")
           print("AFTER LOGIN TOKEN:",get_token(request))

          
           return JsonResponse({
               "success": True,
               "csrftoken": get_token(request)
           })
            #    message= "Login successful",
            #    data={
            #        "username":user.username,
            #        "is_staff": user.is_staff
            #    })
        
           
          
        log_warning(f"Failed login attempt: {username}")


            
        
        return error_response(
                message="invalid credentials",
            
                status_code=400
                )
    
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
   
    permission_classes = [IsAuthenticated]

    def post(self,request):
        print("LOGOUT VIEW HIT")
        logout(request)
        

        return success_response (message="Logged out successfully")

        
        




# # @cache_page(60 * 5)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_categories(request):

    categories = cache.get("categories")

    if categories is None:
        print("CATEGORY CACHE MISS")

        categories = Category.objects.all()

        cache.set(
            "categories",
            categories,
            timeout=300
        )

    else:
        print("CATEGORY CACHE HIT")

    serializer = CategorySerializer(
        categories,
        many=True,
        context={"request": request}
    )

    return Response(serializer.data)







@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])

def user_profile(request):

    print("USER:", request.user)
    print("AUTH:", request.user.is_authenticated)
    
    
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    

    return Response({
        "username":user.username,
        "email":user.email,
        "phone":profile.phone,
        "address":profile.address,
        "city":profile.city,
        "state":profile.state,
        "pincode":profile.pincode
       
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    
    user = request.user
    profile, _= UserProfile.objects.get_or_create(user=user)
    profile.phone = request.data.get("phone")
    profile.address = request.data.get("address")
    profile.city = request.data.get("city")
    profile.state = request.data.get("state")
    profile.pincode = request.data.get("pincode")

    profile.save()
    

    return Response({"message":"Profile updated successfully" })
       
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
# @ratelimit(key='ip', rate='3/m',method='POST', block=True)
def register(request):
    authentication_classes=[]
    print("HEADER TOKEN =", request.META.get("HTTP_x_CSRFTOKEN"))
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({"message":"User created"})




# @method_decorator(cache_page(60 * 5), name="dispatch")
class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    search_fields = ["name", "category__name"]
    filterset_fields = ["category", "price", "stock", "rating"]
    ordering_fields = ["price", "rating", "stock", "created_at"]
    ordering = ["id"]

    def get_queryset(self):
        products = cache.get("products")

        if products is None:
            print("CACHE MISS")
            products = Product.objects.all()
            cache.set("products", products, timeout=300)
        else:
            print("CACHE HIT")

        return products
class OrderInvoiceAPI(APIView):
  
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)

        invoice_number = f"INV-{order.id:05d}"

        print("DEBUG PAYMENT STATUS",order.payment_status)

                # ONLINE → Paid required
        if order.payment_method == "ONLINE":

            if order.payment_status != "PAID":
                return Response(
                    {"error": "Invoice available only after successful payment."},
                    status=400,
                )

        # COD → Delivered required
        elif order.payment_method == "COD":

            if order.status != "DELIVERED":
                return Response(
                    {"error": "Invoice available only after delivery."},
                    status=400,
                )

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        logo_path = os.path.join(settings.BASE_DIR,"store/templates/store/static/logo.png")

        if os.path.exists(logo_path):
            logo = Image(logo_path, width=100, height=50)
            logo.hAlign = "CENTER"
            
        elements.append(Spacer(1,20))

        styles = getSampleStyleSheet()

        from reportlab.lib.enums import TA_CENTER

        center_style = ParagraphStyle(name="Center", alignment=TA_CENTER, fontSize=22)

        elements.append(Paragraph("INVOICE",center_style))
        elements.append(Spacer(1,20))

        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=18,
            textColor=colors.darkblue,
            alignment=1
        )

        company_info = Paragraph(
            "<b>Smart Commerce Pvt Ltd</b><br/>"
            "123 Anna Salai<br/>"
            "Chennai-600002 <br/>"
            "Phone:900000000<br/>"
            "Email:support@smartcommerce.com",
            styles["Normal"]
        )

        logo = None
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1.2*inch, height=0.6*inch)
            header_data = [[company_info, logo]]
            header_table = Table(header_data,colWidths=[4*inch, 2*inch])
            header_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
            elements.append(header_table)
            elements.append(Spacer(1,20))
        elements.append(Paragraph(f"<b>Invoice No:</b> {invoice_number}", styles["Normal"]))
        elements.append(Paragraph(f"<b>GST No:</b>33ABCDE1234F1Z5",styles["Normal"]))
        elements.append(Spacer(1,10))
        elements.append(Paragraph("<b>Bill To:</b>", styles["Heading3"]))
        elements.append(Paragraph(f"{order.user.username}", styles["Normal"]))
        elements.append(Paragraph(f"{order.address}", styles["Normal"]))
        elements.append(Paragraph(f"{order.city}", styles["Normal"]))
        elements.append(Spacer(1,15))
        elements.append(Paragraph(f"OrderDate:{order.created_at.strftime('%d-%m-%Y %H:%M')}", styles["Normal"]))
        elements.append(Paragraph(f"Payment Status:{order.payment_status}", styles["Normal"]))
        elements.append(Spacer(1,20))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        elements.append(Spacer(1,15))
        subtotal = order.total_amount
        gst = subtotal * Decimal("0.18")
        grand_total = subtotal + gst
        data = [["Product", "Qty", "Unit Price","Total"]]


        for item in order.items.all():
            total_price = item.quantity * item.product.price
            data.append([
                item.product.name,
                item.quantity,
                f"${item.product.price:,.2f}",
                f"${total_price:,.2f}"
          ])
            
        subtotal = order.total_amount
        gst = float(subtotal) * 0.18
        grand_total = float(subtotal) + gst

        data.append(["","", "Subtotal", f"$ {subtotal:,.2f}"])
        data.append(["","", "GST (18%)", f"${gst:,.2f}"])
        data.append(["","", "Grand Total", f"${grand_total:,.2f}"])

        table = Table(data, colWidths=[3*inch, 1*inch,1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1, 0), colors.HexColor("#232f3e")),
            ('TEXTCOLOR', (0,0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1,1), (-1, -1), 'CENTER'),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
            ('FONTSIZE',(0,0),(-1,-1),10),
            ('GRID', (0,0), (-1,-1),  0.25, colors.grey),
            ('BACKGROUND', (0,1), (-1, -1), colors.beige),
        ]))

        elements.append(table)

        watermark = ParagraphStyle(
            "watermark",
            fontSize=40,
            textColor=lightgrey,
            alignment=1
        )

        elements.append(Paragraph("SMART COMMERCE", watermark))
        elements.append(Spacer(1,20))
        

        elements.append(Spacer(1,20))
        elements.append(Paragraph("Thank you for shopping with us!", styles["Heading3"]))
        elements.append(Paragraph("This is a computer generated invoice.", styles["Normal"]))

        data = f"{order.id} {order.user.username} {order.total_amount}"

        invoice_hash = hashlib.sha256(data.encode()).hexdigest()
         

        qr_data = f"http://192.168.29.148:8000/api/verify-invoice/{order.id}/?hash={invoice_hash}"

        

        qr = qrcode.make(qr_data)

        qr_path = f"qr_{order.id}.png"
        qr.save(qr_path)

        qr_img = Image(qr_path, width=80, height=80)

        elements.append(Spacer(1,20))
        elements.append(Paragraph("Scan to verify invoice", styles["Normal"]))
        elements.append(Spacer(1,10))
        elements.append(qr_img)
        
                              
        doc.build(elements)
        buffer.seek(0)

        return FileResponse(buffer,as_attachment=True, filename=f"INV-{order.id:05d}.pdf", content_type="application/pdf")
    

def verify_invoice(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        data = f"{order.id} {order.user.username} {order.total_amount}"

        expected_hash = hashlib.sha256(data.encode()).hexdigest()

        received_hash = request.GET.get("hash")

        decoded = base64.b64decode(received_hash).decode()

        if expected_hash != received_hash:
            return render(request,"store/invalid_invoice.html")
        return render(
           request,"store/verify_invoice.html",{"order":order}
        )
    except Order.DoesNotExist:
        return render(request,"store/invalid_invoice.html")


 



      

@api_view(['GET'])
@permission_classes([IsAdminUser])
def revenue_report(request):
    days = int(request.GET.get("days", 7))
    today = timezone.now().date()
    data = []

    for i in range(days -1,-1,-1):
        day = today - timedelta(days=i)
        total = ( Order.objects.filter(
            created_at__date=day,
            payment_status="SHIPPED" 
            
        ).aggregate(total=Sum("total_amount"))
        ["total"] or 0
        )
        

        data.append({
            "date": day.strftime("%Y-%m-%d"),
            "revenue": total
        })
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def revenue_csv(request):
    days = int(request.GET.get("days", 7))
    today = timezone.now().date()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="revenue_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Revenue'])

    for i in range(days -1,-1,-1):
        day = today - timedelta(days=i)
        total = Order.objects.filter(
            created_at__date=day,
            status="SHIPPED"
        ).aggregate(total=Sum("total_amount"))["total"] or 0
        
        

        writer.writerow([day.strftime("%Y-%m-%d"),
            total])
        
    return response

class MonthlyReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
      last_30_days = now() - timedelta(days=30)

      orders = Order.objects.filter(
          created_at__gte=last_30_days,
          payment_status="PAID"
      )

      total_revenue = orders.aggregate(
          total=Sum("total_amount"))["total"] or 0
      
      return Response({
          "monthly_revenue": total_revenue,
          "orders_count": orders.count()
      })
    

class AdminRefundAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self,request, order_id):
      
      order = get_object_or_404(Order, id=order_id)
      action = request.data.get("action")

      if order.refund_status !="REQUESTED":
          return Response({"error": "Refund not requested"}, status=400)
      
      if action == "approve":
          order.refund_status = "COMPLETED"
      elif action == "reject":
         order.refund_status = "REJECTED"
      else:
        return Response({"error": "Invalid action"}, status=400)

      
      order.save()
        

      return success_response(message=f"Refund {order.refund_status}")
    


       
      

class OrderCreateAPIView(APIView):
    
   
    permission_classes = [IsAuthenticated]

   
    def post(self, request):

        try:
            items = request.data.get("items",[])
            amount = request.data.get("amount", 0)
            address = request.data.get("address")
            payment_method = request.data.get("payment_method", "COD")

            if not address:
                return Response(
                    {"error": "Address is required"},
                    status=400
                )
            

            if len(address) < 10:
                return Response(
                    {"error": "Address too short"},
                    status=400
                )
            

            if payment_method not in ["COD", "ONLINE"]:
                return Response(
                    {"error": "Invalid payment method"},
                    status=400
                )
            
            if not items:
                return Response(
                    {"error": "Cart is empty"},
                    status=400
                )
            


            payment_method = str(payment_method).strip().upper()

            print("PAYMENT METHOD =", payment_method)

            print("FULL REQUEST =", request.data)
            if payment_method == "COD" and not items:
                    return Response({"error": "No items "}, status=400)
            
            total = 0

            if payment_method == "COD":

                    print("STEP 1")
                    
                

            
                    order = Order.objects.create(
                        user=request.user,
                        address=address,
                        payment_method="COD",
                        payment_status="PENDING",
                        status="PLACED",
                        total_amount=0 
                    )

                    total = 0

                    print("STEP 2 ORDER CREATED")
                
                    
                    for item in items:

                        print("STEP 3 LOOP START")

                        print("ITEM DATA =", item)
                    
                        product_id = item.get("product_id")

                        print("PRODUCT ID =", product_id)

                        # if not product_id and item.get("product"):
                        #     product_id = item["product"]["id"]

                        # try:

                        product = Product.objects.get(id=product_id)

                        qty = int(item.get("quantity", 1))

                        # Check stock before placing order
                        if product.stock < qty:
                            return Response(
                                {
                                    "error": f"{product.name} has only {product.stock} items left"
                                },
                                status=400
                            )

                        price = product.price * qty

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=qty,
                            price=price
                        )

                        # Reduce stock
                        product.stock -= qty
                        product.save()

                        total += price

                    order.total_amount = total

                    order.save()

                    

                    # Clear Redis cache because product stock has changed
                    cache.delete("products")

                    log_info(f"Order {order.id} created by {request.user.username}")

                    # send_order_email.delay(order.user.email, order.id)

                    html = f"""
                    <h2>🎉 Order Confirmed</h2>

                    <p>Thank you for shopping with <b>Smart Shop</b>.</p>

                    <p>Your Order ID is <b>#{order.id}</b>.</p>

                    <p>Your order has been received successfully.</p>

                    <p>We will notify you when your order is processed and shipped.</p>
                    """

                    send_resend_email(
                        to_email=order.user.email,
                        subject=f"Order #{order.id} Confirmed",
                        html_content=html,
                    )
                    # send_invoice_email_task.delay(order.id)

                    

                    

                    print("STEP 4 ITEM CREATED")
                    #     print(request.data)
                    #     print("ORDER SAVED:", order.id)

                
                    

                    cart_items = CartItem.objects.filter(cart__user=request.user)

                    # print("CART ITEMS:", cart_items.count())

                    print("STEP 5 BEFORE DELETE")

                    cart_items.delete()

                    print("STEP 6 AFTER DELETE")

                    # print("SKIPPED CART DELETE")


                    # print("ORDER CREATED")
                    # print("ORDER ID", order.id)


                    print("STEP 7 RETURNING RESPONSE")

                    return success_response(
                      message="Order placed successfully",
                      data={"order_id": order.id},
                      status_code=201)
        except Exception as e:
            

            log_error(str(e))

            return Response({
                "error": str(e)
            }, status=500)
            return Response({
                "error": str(e)
            }, status=500)

            
            


                # if payment_method == "ONLINE":
                        


                            
            
                        

                #     try:
                #         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

                        

                        


                #         payment = client.order.create({
                #             "amount": amount,
                #             "currency":"INR",
                #             "payment_capture": 1
                #         })
                        
                    
                
            
                
                #         return Response({
                                
                        
                #             "razorpay_order_id":payment["id"],
                #             "amount": amount
                #         })
                #     except Exception as e:

                        
                #         return Response({"error": str(e)}, status=400)
            

                


class CreatePaymentOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

      
    def post(self,request):
      
      amount = request.data.get("amount")

      if not amount:
          return Response({"error":"Amount missing"}, status=400)
      

      client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

      try:
      
         payment = client.order.create({
                'amount': int(float(amount) * 100),
                 'currency':"INR",
                 'payment_capture': 1,
                 
         
          })
      


         return success_response(
             message="Payment order created",
             data={
                 "razorpay_order_id":payment["id"],
                  "amount": amount
            }
         )
      except Exception as e:
          
          import traceback
          log_error(traceback.format_exc())
          
          return Response({"error": str(e)}, status=400)


                    


# @method_decorator(ratelimit(key='ip', rate='10/m',method='POST',block=True),name='post')
class VerifyPaymentAPIView(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self,request):

        cart_items = CartItem.objects.filter(cart__user=request.user)
        
        order_id = request.data.get("order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_signature = request.data.get("razorpay_signature")
       
       

        if not all([order_id, razorpay_payment_id, razorpay_order_id, razorpay_signature]):
            return Response({"error": "Missing payment data"}, status=400)
    
        
        

        try:

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            params = {
                "razorpay_order_id":
                razorpay_order_id,
                "razorpay_payment_id":
                razorpay_payment_id,
                "razorpay_signature":
                razorpay_signature
            }
             
            #client.utility.verify_payment_signature(params)


            order = Order.objects.create(
                user=request.user,
                address="Chennai Tamil Nadu India",
                # payment_method="ONLINE",
                payment_status="PAID",
                status="PLACED",
                total_amount=0 
            )
            
            total = 0

                                    

            
                                    
           

            for item in cart_items:
                product = item.product
                qty = item.quantity
                price = product.price * qty

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=price
                )
            
           
                total += price

            order.total_amount = total
            order.save()

            log_info(f"Payment successful for Order {order.id}")


      

       

            CartItem.objects.filter(cart__user=request.user).delete()

            return success_response(message="Payment successful")
        except Order.DoesNotExist:
            return Response({"error":"Order not found"}, status=404)
        
        except razorpay.errors.SignatureVerificationError:
            return Response({"error":"Payment verification failed"}, status=400)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)
       


        


class CartDetailAPIView(APIView):
   
    permission_classes = [IsAuthenticated]

    def get(self, request):
      from .serializers import CartSerializer

      cart, _ = Cart.objects.get_or_create(user=request.user)
      serializer = CartSerializer(cart)
      return success_response(
          message="Cart fetched successfully",
          data=serializer.data)
    




    
# @method_decorator(csrf_exempt, name="dispatch")
class AddToCartAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self,request,product_id):

        print("ADD TO CART VIEW ENTERED")

        print("-" * 60)
        print("PATH:", request.path)
        print("METHOD:", request.method)
        print("COOKIES:", request.COOKIES)
        print("CSRF HEADER:", request.META.get("HTTP_X_CSRFTOKEN"))
        print("ORIGIN:", request.META.get("HTTP_ORIGIN"))
        print("REFERER:", request.META.get("HTTP_REFERER"))
        print("=" * 60)

        print("ADD TO CART HIT")
        print("USER =", request.user)
        print("IS AUTH =", request.user.is_authenticated)        
        product = get_object_or_404(Product, id=product_id)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        quantity = int(request.data.get("quantity",1))
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if item.quantity + quantity > product.stock:
            return Response({"error":"Out of stock"}, status=400)

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity
            item.save()

        return success_response(message= "Item added to cart")
    
@method_decorator(csrf_exempt, name="dispatch")
class DecreaseCartItemAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,product_id):
        
        product = get_object_or_404(Product, id=product_id)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        item = CartItem.objects.filter(cart=cart, product=product).first()

        if item:
            if item.quantity > 1:
               item.quantity -= 1
               item.save()
            else:
            
               item.delete()

        return success_response(message= "Quantity decreased")
    
@method_decorator(csrf_exempt, name="dispatch")
class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, item_id):
        CartItem.objects.filter(
          id=item_id, 
          cart__user=request.user
         ).delete()
        
        return success_response(message="Item removed from  cart")
    


# @method_decorator(cache_page(60 * 5), name="dispatch")
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class MyOrdersAPIView(APIView):
    

    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")

        data = []

        for order in orders:
            items = []

            for item in order.items.all():

                items.append({
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "price":item.price,
                    "subtotal": item.price * item.quantity,
                })
            data.append({
                "id": order.id,
                "total":order.total_amount,
                "status":order.status,
                "payment":order.payment_method,
                "payment_method":order.payment_method,
                "payment_status": order.payment_status,
                "placed_at": order.placed_at,
                "packed_at": order.packed_at,
                "shipped_at":order.shipped_at,
                "delivered_at":order.delivered_at,
                "cancelled_at": order.cancelled_at,
                "refund_status":order.refund_status,
                "return_status":order.return_status,
                "items":items

            })

        return success_response(message="Order fetched successfully",data=data)
       
    

class CancelOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, order_id):
        try:
           order = Order.objects.get(id=order_id,user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"},status=404)
        
        if order.status not in ["PLACED", "PROCESSING"]:
            return Response(
                {"error": "Only PLACED or PROCESSING orders can be cancelled"},
                status=400
            )
            
        
       
        order.status = "CANCELLED"
        order.cancelled_at = timezone.now()

        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        if order.payment_status == "PAID":
           order.refund_status = "REQUESTED"
        else:
           order.refund_status = "NOT_REQUIRED"
        
        
        order.cancel_reason = request.data.get("reason","")
        order.save()

        cache.delete("orders")
        cache.delete("products")

        log_info(f"Order {order.id} cancelled by {request.user.username}")
        

        return success_response(message= "Order Cancelled successfully")
       
           
        


class UpdateOrderStatusAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, order_id):
       order = get_object_or_404(Order, id=order_id)


       new_status = request.data.get("status")

       allowed_status = ["PROCESSING", "SHIPPED", "DELIVERED"]

       if new_status not in allowed_status:
          return Response({"error": "Invalid status"}, status=400)
       order.status = new_status
       order.save()

       cache.delete("orders")

      

       if new_status == "DELIVERED":
           send_invoice_email(order.id)
            # send_invoice_email_task.delay(order.id)


       
        
           
       return success_response(
          message=f"Order updated to {new_status}"
                
        )
    

class AdminOrdersAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        
      orders = Order.objects.all().order_by("-created_at")
      serializer = OrderSerializer(orders, many=True)
        
      return success_response(
          message="Order fetched successfully",
          data=serializer.data
      )
    

class AdminUpdateOrderAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
             return Response({"error": "Order not found"},status=404)
        
        order.status = request.data.get("status",order.status)
        order.payment_status = request.data.get("payment_status",order.payment_status,order.payment_status)
        order.refund_status = request.data.get("refund_status",order.refund_status,order.refund_status)

        order.save()
       
        
           
        return success_response(
                message="Order updated by Admin"
                
        )
    

class AdminDashboardStateAPIView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get(self, request):
        
        total_orders = Order.objects.count()
        total_users = User.objects.count()
        total_revenue = Order.objects.filter(
            payment_status="PAID"
        ).aggregate(total=Sum("total_amount"))["total"] or 0

        shipped_orders = Order.objects.filter(status="SHIPPED").count()
        cancelled_orders = Order.objects.filter(status="CANCELLED").count()
        pending_orders = Order.objects.filter(status="PLACED").count()

        
        
           
        return success_response(
            message="Dashboard stats fetched",
            data={
                "total_orders": total_orders,
                "total_users": total_users,
                "total_revenue": total_revenue,
                "shipped_orders": shipped_orders,
                " cancelled_orders":  cancelled_orders,
                " pending_orders " :  pending_orders 
                              
            }
        )
    
    
class AdminOrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, order_id):
     
      
      order = get_object_or_404(Order, id=order_id)
      
      serializer = OrderSerializer(order)
            
           
            
         
      return success_response(
          message="Order fetched successfully",
          data=serializer.data
      )
    
class OrderDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
      
      
      
      try:
            order = Order.objects.get(pk=pk, user=request.user)
      except Order.DoesNotExist:
             return error_response(
                 message= "Order not found",status_code=404)
      
      serializer = OrderSerializer(order)
            
           
            
         
      return success_response(
          message="Order fetched successfully",
          data=serializer.data)
    
        

class AdminTopProductsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
      from store.models import OrderItem
        
      top_products = (
          OrderItem.objects
          .values("product__name")
          .annotate(
              total_sold=Sum("quantity"),
              total_revenue=Sum("price")
          )
          .order_by("-total_sold")
      )
        
        
        
           
      return Response(top_products)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])

def pay_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)

        if order.status == "CANCELLED":
            return Response({"error": "Order cancelled"}, status=400)
        
        order.payment_status = "PAID"
        order.status = "PROCESSING"
        order.save()

        return success_response(message= "Payment successful")
    
    except Order.DoesNotExist:
        return error_response(message= "Order not found", status_code=404)
  

    


class RequestReturnAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,order_id):
        print("RETURN API HIT")

        order = get_object_or_404(Order,id=order_id, user=request.user)

        if order.status != "DELIVERED":
           return Response({"error": "Return allowed only for delivered orders"}, status=400)
        
        if order.return_status != "NONE":
           return Response({"error": "Return already requested"}, status=400)
        
        order.return_status = "REQUESTED"
        order.save()
        
        
        return success_response(message= "Return requested successfully")
    


class RefundDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )

        if order.payment_method != "COD":
            return Response(
                {"error": "Refund details required only for COD orders"},
                status=400
            )

        order.refund_account_name = request.data.get("account_name")
        order.refund_account_number = request.data.get("account_number")
        order.refund_ifsc = request.data.get("ifsc")
        order.refund_upi_id = request.data.get("upi_id")

        
        order.save()

        return success_response(
            message="Refund details saved successfully"
        )

    

from django.http import JsonResponse

def ratelimit_error(request, exception):

    return JsonResponse({
        "success": False,
        "message": "Too many requests. Please try again later."
    }, status=420)
    



    
    






        
         
        
    




                            
