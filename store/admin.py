from django import forms
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

class OrderAdminForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Payment PAID இல்லையென்றால் DELIVERED option காட்ட வேண்டாம்
        if self.instance and self.instance.payment_status != "PAID":
            self.fields["status"].choices = [
                choice
                for choice in self.fields["status"].choices
                if choice[0] != "DELIVERED"
            ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   form = OrderAdminForm
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

    print("ADMIN SAVE_MODEL HIT")

    old_status = None

    if change:
        old_status = Order.objects.get(pk=obj.pk).status

    # --------------------------------
    # PAYMENT VALIDATION
    # --------------------------------
    if obj.status == "DELIVERED" and obj.payment_status != "PAID":
        from django.core.exceptions import ValidationError

        raise ValidationError(
            "Order cannot be marked as DELIVERED until payment is PAID."
        )

    # --------------------------------
    # TIMESTAMPS
    # --------------------------------
    if obj.status == "PACKED" and not obj.packed_at:
        obj.packed_at = timezone.now()

    elif obj.status == "SHIPPED" and not obj.shipped_at:
        obj.shipped_at = timezone.now()

    elif obj.status == "DELIVERED" and not obj.delivered_at:
        obj.delivered_at = timezone.now()

    super().save_model(request, obj, form, change)

    print("AFTER SAVE")
    print("STATUS =", obj.status)

    # --------------------------------
    # STATUS CHANGED
    # --------------------------------
    if change and old_status != obj.status:

        print("STATUS CHANGED")

        # --------------------------------
        # DELIVERED
        # --------------------------------
        if obj.status == "DELIVERED":

            # COD + PAID → Delivered + Invoice
            if (
                obj.payment_method == "COD"
                and obj.payment_status == "PAID"
            ):
                send_invoice_email(obj.id)

            # ONLINE + PAID
            # OR COD + PENDING
            # → Delivered email WITHOUT invoice
            else:

                if obj.user.email:

                    html = f"""
                    <h2>📦 Order Delivered</h2>

                    <p>Hello <b>{obj.user.username}</b>,</p>

                    <p>
                        Your Order <b>#{obj.id}</b>
                        has been successfully delivered.
                    </p>

                    <p>
                        Thank you for shopping with
                        <b>Smart Commerce</b>.
                    </p>

                    <br>

                    <p>
                        Thank you,<br>
                        <b>Smart Commerce Team</b>
                    </p>
                    """

                    send_resend_email(
                        to_email=obj.user.email,
                        subject=f"Order #{obj.id} Delivered",
                        html_content=html,
                    )

        # --------------------------------
        # OTHER STATUSES
        # PROCESSING / PACKED / SHIPPED
        # --------------------------------
        else:

            if obj.user.email:

                html = f"""
                <h2>Order Status Updated</h2>

                <p>Hello <b>{obj.user.username}</b>,</p>

                <p>
                    Your Order <b>#{obj.id}</b>
                    status has been updated.
                </p>

                <h3>Status: {obj.status}</h3>

                <p>
                    Thank you for shopping with Smart Commerce.
                </p>
                """

                send_resend_email(
                    to_email=obj.user.email,
                    subject=f"Order #{obj.id} - {obj.status}",
                    html_content=html,
                )


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)

