from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models import Order
from django.shortcuts import get_object_or_404

def send_invoice_email(order_id):

    order = Order.objects.prefetch_related("items__product").get(id=order_id)
    template= get_template("store/invoice.html")
    items = order.items.all()

    subtotal = 0
    for item in items:
        subtotal += float(item.price) * item.quantity

        cgst = subtotal * 0.09
        sgst = subtotal * 0.09
        grand_total = subtotal + cgst + sgst
    
   
   
    html = template.render({
        "order":order,
        "items":items,
        "subtotal": subtotal,
        "cgst": cgst,
        "sgst": sgst,
        "grand_total": grand_total,
        "logo_path":"templates/store/static/logo.png"
    })

    pdf_file = BytesIO()
    pisa.CreatePDF(html, dest=pdf_file)
    pdf_file.seek(0)

             
      
    email = EmailMessage(
         subject= f" Invoice - Order #{order.id}",
         body='Hi,Please find attached your invoice.Thank you for shopping with us.',

         from_email=settings.DEFAULT_FROM_EMAIL, 
         to=[order.user.email],
       
           )
        
         

    email.attach(
       f"invoice_{order.id}.pdf",pdf_file.getvalue(),
        
        "application/pdf"
    )

    email.send()
   

    


    