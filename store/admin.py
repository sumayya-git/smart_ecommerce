from django.contrib import admin
from django.utils import timezone
from django.core.mail import send_mail
from .models import Category, Product, Order, OrderItem
from django.utils.html import format_html

from .utils import send_invoice_email

from .api.resend import send_resend_email


class Orderiteminline(admin.TabularInline):
   model = OrderItem
   extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display = ("id", "user",  "status", "colored_return_status","payment_status","payment_method","colored_refund_status","total_amount", "created_at")

   fields = (
      "user",
      "status",
      "payment_status",
      "payment_method",
      "return_status",
      "refund_status",
      "total_amount",
   )
   list_filter = ("status","payment_status","payment_method", "return_status","refund_status")
   inlines = [Orderiteminline]

   readonly_fields = (
      "placed_at",
      "packed_at",
      "shipped_at",
      "delivered_at",
      "created_at",
   )

   def get_readonly_fields(self, request, obj=None):
       if obj and obj.status == "DELIVERED":
        return ["user","total_amount","payment_status", "payment_method", "placed_at","packed_at","shipped_at","delivered_at"]
       return self.readonly_fields
   def has_delete_permission(self, request, obj=None):
      if obj and obj.status == "DELIVERED":
         return False
      return True
   

   def colored_return_status(self, obj):

    if obj.return_status == "REQUESTED":
        color = "red"

    elif obj.return_status == "APPROVED":
        color = "green"

    elif obj.return_status == "REJECTED":
        color = "darkred"

    else:   # NONE
        color = "gray"

    return format_html(
        '<b><span style="color:{};">{}</span></b>',
        color,
        obj.get_return_status_display()
    )

   colored_return_status.short_description = "Return Status"


   def colored_refund_status(self, obj):

    if obj.refund_status == "INITIATED":
        color = "orange"

    elif obj.refund_status == "COMPLETED":
        color = "green"

    elif obj.refund_status == "REJECTED":
        color = "red"

    else:   # NOT_INITIATED
        color = "gray"

    return format_html(
        '<b><span style="color:{};">{}</span></b>',
        color,
        obj.get_refund_status_display()
    )

   colored_refund_status.short_description = "Refund Status"
   
   
   def save_model(self, request, obj, form, change):
     
     old_status = None

     if change:
        old_status = Order.objects.get(pk=obj.pk).status
    #obj.refresh_from_db()

    #updated_fields = []

   
     if obj.status == 'PACKED' and not obj.packed_at:
         obj.packed_at = timezone.now()
         #updated_fields.append("packed_at")

              
     elif obj.status == 'SHIPPED' and not obj.shipped_at:
           obj.shipped_at = timezone.now()
          # updated_fields.append("shipped_at")

     elif obj.status == 'DELIVERED' and not obj.delivered_at:
           obj.delivered_at = timezone.now()


     super().save_model(request, obj, form, change)

     if change and old_status != obj.status:
      # send_resend_email(...)

            

      if obj.status == "DELIVERED":
            send_invoice_email(obj.id)

            if obj.user.email:

                html = f"""
                <h2>Order Status Updated</h2>

                <p>Hello <b>{obj.user.username}</b>,</p>

                <p>Your Order <b>#{obj.id}</b> status has been updated.</p>

                <h3>Status: {obj.status}</h3>

                <p>Thank you for shopping with Smart Commerce.</p>
                """

                send_resend_email(
                    to_email=obj.user.email,
                    subject=f"Order #{obj.id} Status Updated",
                    html_content=html,
                )

    #  if obj.user.email:
    #         send_mail(
    #            subject=f"Order #{obj.id} Status Update",
    #            message=f"Your order status is now: {obj.status}",
    #            from_email='smartshop.notify@gmail.com',
    #            recipient_list=[obj.user.email],
    #            fail_silently=True
    #         )

   
           #updated_fields.append("delivered_at")

    #if updated_fields:
    # obj.save(update_fields=updated_fields)

    #  if obj.user.email:

    #   send_mail(
    #     subject=f"Order #{obj.id} Status Update",
    #     message=f"Your order status is now: {obj.status}",
    #     from_email='smartshop.notify@gmail.com',
    #     recipient_list=[obj.user.email],
    #     fail_silently=True
      
    #    )


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)

