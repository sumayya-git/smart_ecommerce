from django.contrib import admin
from django.utils import timezone
from django.core.mail import send_mail
from .models import Category, Product, Order, OrderItem


class Orderiteminline(admin.TabularInline):
   model = OrderItem
   extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display = ("id", "user",  "status", "payment_status","payment_method","refund_status","total_amount", "created_at")

   fields = (
      "user",
      "status",
      "payment_status",
      "payment_method",
      "return_status",
      "refund_status",
      "total_amount",
   )
   list_filter = ("status","payment_status","payment_method", "refund_status")
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
   
   
   def save_model(self, request, obj, form, change):
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

   
           #updated_fields.append("delivered_at")

    #if updated_fields:
    # obj.save(update_fields=updated_fields)

     if obj.user.email:

      send_mail(
        subject=f"Order #{obj.id} Status Update",
        message=f"Your order status is now: {obj.status}",
        from_email='smartshop.notify@gmail.com',
        recipient_list=[obj.user.email],
        fail_silently=True
      
       )


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)

