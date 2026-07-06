from celery import shared_task


from django.core.mail import send_mail
from django.conf import settings

from store.utils import send_invoice_email





@shared_task
def send_order_email(customer_email, order_id):
    send_mail(
        subject=f"Order #{order_id} Confirmed",
        message=f"Thank you for your order.\n\nYour Order ID is {order_id}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[customer_email],
        fail_silently=False,
    )

    return "Email Sent Successfully"


@shared_task
def test_task():
    print("✅ Celery is working!")
    return "Success"



@shared_task
def send_invoice_email_task(order_id):
    send_invoice_email(order_id)
    return "Invoice Email Sent Successfully"