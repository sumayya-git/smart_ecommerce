from celery import shared_task

from store.api.resend import send_resend_email
from store.utils import send_invoice_email


@shared_task
def send_order_email(customer_email, order_id):
    """
    Send Order Confirmation Email
    """

    html = f"""
    <h2>🎉 Order Confirmed</h2>

    <p>Thank you for shopping with <b>Smart Shop</b>.</p>

    <p>Your Order ID is <b>#{order_id}</b>.</p>

    <p>Your order has been received successfully.</p>

    <p>We will notify you when your order is processed and shipped.</p>
    """

    try:
        send_resend_email(
            to_email=customer_email,
            subject=f"Order #{order_id} Confirmed",
            html_content=html,
        )

        print(f"✅ Order email sent to {customer_email}")

        return "Order Email Sent Successfully"

    except Exception as e:
        print("❌ Order Email Error:", str(e))
        raise


@shared_task
def send_invoice_email_task(order_id):
    """
    Send Invoice PDF Email
    """

    try:
        send_invoice_email(order_id)

        print(f"✅ Invoice email sent for Order #{order_id}")

        return "Invoice Email Sent Successfully"

    except Exception as e:
        print("❌ Invoice Email Error:", str(e))
        raise


@shared_task
def test_task():
    """
    Test Celery Worker
    """

    print("✅ Celery is working!")

    return "Success"