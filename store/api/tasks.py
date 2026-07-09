from celery import shared_task

from store.api.brevo import send_brevo_email
from store.utils import send_invoice_email


@shared_task
def send_order_email(customer_email, order_id):

    html = f"""
    <h2>Order Confirmed 🎉</h2>

    <p>Thank you for shopping with <b>Smart Shop</b>.</p>

    <p>Your Order ID is <b>#{order_id}</b>.</p>

    <p>Your order has been received successfully.</p>
    """

    send_brevo_email(
        to_email=customer_email,
        subject=f"Order #{order_id} Confirmed",
        html_content=html,
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