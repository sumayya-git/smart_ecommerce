from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import redirect
from decimal import Decimal
from .models import Category,Product, Order
from .models import OrderItem
from io import BytesIO
import os
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.staticfiles import finders
from store.utils import send_invoice_email
from .models import CartItem
from rest_framework.authentication import SessionAuthentication


STATUS_FLOW = ["PLACED","PAID","SHIPPED","DELIVERED","CANCEL_REQUESTED","CANCELLED",]


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    
    return render(request, 'store/home.html',{'products':products,'categories': categories,'active_category':'all'})


def category_products(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    
    return render(request, 'store/category_products.html',{'category': category,
        'products': products, 'categories': categories, 'active_category': category.slug })


@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)

    data = []
    total = 0

    for item in items:
        subtotal = item.product.price * item.quantity
        total += subtotal

        data.append({
            "product": item.product.name,
            "price": item.product.price,
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return JsonResponse({"items": data, "total": total})


@login_required
def add_to_cart(request):
    

    product_id = request.POST.get(product_id)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product_id=product_id
    )


    if not created:
        item.quantity += 1
        item.save()

    return JsonResponse({"message": "Added to cart"})

def remove_from_cart(request):
     product_id = request.POST.get(product_id)

     CartItem.objects.filter(user=request.user,
                             product_id=product_id).delete()
   
     return JsonResponse({"message":"Removed"})


def increase_qty(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
        
        
    request.session['cart'] = cart
    return redirect('cart')


def decrease_qty(request, id):
    cart = request.session.get('cart', {})
    if cart[str(id)] > 1:
        cart[str(id)] -= 1
    else:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def reduce_item_qty(request, item_id):
    item = OrderItem.objects.get(id=item_id)

    if item.order.status in["PLACED", "PACKED"]:
        if item.effective_qty() > 1:
            item.cancelled_qty += 1
            item.save()

    return redirect("track_order", item.order.id)

@login_required
def reduce_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)

    if item.order.user != request.user:
        return redirect("my_orders")
    
   
    
    if item.order.status in["PLACED", "PACKED"]:
        if item.effective_qty() > 1:
            item.cancelled_qty += 1
            item.save()

    order = item.order
    total = 0

    for i in order.items.all():
        total += i.effective_qty() * i.price

    order.total_amount = total
    order.save()

    return redirect("track_order", order.id)

@login_required
def increase_order_item(request, item_id):
  item = get_object_or_404(OrderItem, id=item_id)

  if item.order.user != request.user:
     return redirect("my_orders")
    
   
    
  if item.order.status != "PLACED" or item.order.payment_status == "PAID":
     return redirect("track_order", item.order.id)
  if item.cancelled_qty > 0:
     item.cancelled_qty -= 1
  else:
     item.quantity +=1
     item.save()

     order = item.order
     order.total_amount = sum(i.effective_qty() * i.price for i in order.items.all())
     total = 0

    
     order.save()

     return redirect("track_order", order.id)
@login_required
def checkout(request):
    cart = request.session.get('cart',{})

    cart_items = []
    total = Decimal('0.00')


    for pid, qty in cart.items():
          product = Product.objects.get(id=pid)
          subtotal = product.price * qty
         
          total += subtotal

          cart_items.append({
              'product': product,
              'qty': qty,
              'subtotal': subtotal
          })
    
    return render(request, 'store/checkout.html',
                  {
                      'cart_items': cart_items,
                      'total': total
                  })
    
@login_required
def place_order(request):
       
  if request.method != "POST":
     return redirect('checkout')
  address = request.POST.get("address")
  city = request.POST.get("city")
  state = request.POST.get("state")
  pincode =request.POST.get("pincode")
  phone = request.POST.get("phone")
     
  cart = request.session.get('cart')
  if not cart:
     return redirect('cart')
        
  total = Decimal('0.00')
          
       
  
  for pid, qty in cart.items():
    product = Product.objects.get(id=int(pid))
    total += product.price * int(qty)
             
         

  order = Order.objects.create(
    user=request.user,
    total_amount=total,
    address=address,
    city=city,
    state=state,
    pincode=pincode,
    phone=phone,
    status="PLACED"
  )

  print("ORDER SAVED ID",order.id)

  for pid, qty in cart.items():
    product = Product.objects.get(id=int(pid))
    qty = int(qty)
    OrderItem.objects.create(
       order=order,
       product=product,
       quantity=qty,
       price=product.price
    )
               
           

  request.session['cart'] = {}
  request.session.modified = True

  print("ORDER Id", order.id)

  return render(request,'store/success.html', { 
    'order': order, 
    'order_id': order.id
   })





@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    items = order.items.all()

    return render(request,'store/order_detail.html', {
        'order': order,
        'items': order.items.all(),
        'RAZOORPAY_KEY_ID': settings.RAZOORPAY_KEY_ID,
    })

   

def order_status(request):
    order = None
    error = None

    if request.method == "POST":
        order_id = request.POST.get('order_id')

        if order_id:
           try:
              order = Order.objects.get(id=order_id)
           except Order.DoesNotExist:
              error = "indha Order ID kidaikavillai"
        else:
            error = "Order ID enter pannunga"
            
    return render(request, "store/order_status.html", {"order": order, "error": error})

# STATUS_FLOW = ['PLACED','PACKED', 'SHIPPED','CANCEL_REQUESTED', 'DELIVERED',]

@login_required
def track_order(request, order_id):
    order =get_object_or_404(Order,id=order_id, user=request.user)

    STATUS_FLOW = ['PLACED','PACKED', 'SHIPPED', 'DELIVERED',]

    
    items = []
    grand_total = 0

    for item in order.items.all():
        qty = item.effective_qty()
        subtotal = qty * item.price
        grand_total += subtotal

        items.append({
            "product": item.product,
            "price": item.price,
            "qty": qty,
            "subtotal": subtotal,
        })

        if order.status == "CANCEL_REQUESTED":
           current_index = STATUS_FLOW.index("PLACED")
           cancel_index = STATUS_FLOW.index("DELIVERED")

        elif order.status == "CANCELLED":
            current_index = None
            cancel_index = None
       
        else:
             current_index = STATUS_FLOW.index(order.status)
             cancel_index = None

               
       
              
    return render(request, "store/track_order.html", {
        "order": order, 
        "items": items,
        "grand_total": grand_total,
        "status_flow": STATUS_FLOW,
        "current_index": current_index,
        "cancel_index": cancel_index,
        "RAZORPAY_KEY_ID":
        settings.RAZORPAY_KEY_ID
                                                             
         })

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user= User.objects.create_user(username=username, email=email,password=password)
            
        user.save()

        login(request, user)
        return redirect('home')
    
    return render(request, 'store/signup.html')


def login_view(request):
    if request.method == 'POST':
     
    
     username = request.POST.get("username")
     password = request.POST.get("password")

     user = authenticate(request, username=username, password=password)

     if user is not None:
            login(request, user)
            return JsonResponse({"message":"Login success"})

            
     else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
                
    
   


def logout_view(request):
    logout(request)
    return redirect('home')

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'store/product_detail.html', {
        'product': product
    })

# Create your views here.

def link_callback(url, rel):
    if url.startswith(settings.STATIC_URL):
        path= os.path.join(settings.BASE_DIR,'store', 'templates','store','static', url.replace(settings.STATIC_URL,''))
        return path
    return url

def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if order.payment_status == "PAID" and not order.invoice_sent:
        send_invoice_email(request, order.id)
        order.invoice_sent = True
        order.save()
    return render(request, 'store/success.html',
{
    'order': order
   })




def get_cart_count(request):
    cart = request.session.get('cart',{})
    return sum(cart.values())



@login_required
def remove_item(request):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == "CANCELLED":
        return redirect("track_order", order_id=order.id)
    
    
    if order.payment_status == "PAID":
       order.status = "CANCEL_REQUESTED"
       order.refund_status = "PENDING"
       order.save()

       messages.success(
           request, "Cancellation request received. Refund will be processed within 3-5 working days."
       )
       return redirect("track_order", order_id=order.id)
    
       order.status = "CANCELLED"
       order.refund_status = "NOT_APPLICABLE"
       order.save()

    return redirect("track_order", order_id=order.id)



    

def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = []
    subtotal_total = Decimal("0.00")


    for item in OrderItem.objects.filter(order=order):
        qty = item.effective_qty()
        if qty <=0:
            continue

        subtotal = item.price * qty
        subtotal_total += subtotal

        items.append({
        "product": item.product,
        "price": item.price,
        "qty": qty,
        "subtotal": subtotal,
        })

    gst_rate = Decimal('0.18')
    gst_amount = subtotal_total * gst_rate
    cgst = gst_amount / Decimal('2')
    sgst = gst_amount / Decimal('2')
    grand_total = subtotal_total + gst_amount


    template = get_template("store/invoice.html")
    html = template.render({
    "order": order,
    "items": items,
    "subtotal": subtotal_total,
    'cgst': cgst,
    'sgst': sgst,
    'gst_amount': gst_amount,
    'grand_total': grand_total,
    'is_cancelled': order.status == "CANCELLED",
    "refund_completed": (
    order.status == "CANCELLED" and order.refund_status == "COMPLETED"
    ),
    "logo_path":finders.find("logo.png"),
    })

    result = BytesIO()
    pdf = pisa.CreatePDF(html, dest=result)

    if pdf.err:
        return HttpResponse("PDF generation error", status=500)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'

    if not order.invoice_sent:
      email = EmailMessage(
         subject='Your Invoice - Smart E-Commerce',
         body='Hi,\n\nPlease find attached your invoice.\n\n Thank you for shopping with us.',
         from_email=settings.EMAIL_HOST_USER, 
         to=[order.user.email],
            )
      email.attach('invoice.pdf',result.getvalue(),'application/pdf')
      email.send()
      order.invoice_sent = True
      order.save()

    return response



  






    