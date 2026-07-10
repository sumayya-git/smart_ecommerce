from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders

from io import BytesIO
import base64

from xhtml2pdf import pisa
import requests

from .models import Order


def send_invoice_email(order_id):

    order = Order.objects.prefetch_related(
        "items__product"
    ).get(id=order_id)

    template = get_template("store/invoice.html")

    items = order.items.all()

    subtotal = 0

    for item in items:
        subtotal += float(item.price) * item.quantity

    cgst = subtotal * 0.09
    sgst = subtotal * 0.09
    grand_total = subtotal + cgst + sgst

    logo_path = finders.find("logo.png")

    html = template.render({
        "order": order,
        "items": items,
        "subtotal": subtotal,
        "cgst": cgst,
        "sgst": sgst,
        "grand_total": grand_total,
        "logo_path": logo_path,
    })

    pdf_buffer = BytesIO()

    pisa.CreatePDF(html, dest=pdf_buffer)

    pdf_buffer.seek(0)

    pdf_base64 = base64.b64encode(
        pdf_buffer.read()
    ).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "from": "Smart Shop <onboarding@resend.dev>",
        "to": [order.user.email],
        "subject": f"Invoice - Order #{order.id}",
        "html": """
            <h2>Invoice Attached</h2>
            <p>Thank you for shopping with Smart Shop.</p>
            <p>Your invoice is attached as a PDF.</p>
        """,
        "attachments": [
            {
                "filename": f"invoice_{order.id}.pdf",
                "content": pdf_base64,
            }
        ],
    }

    response = requests.post(
        "https://api.resend.com/emails",
        headers=headers,
        json=data,
        timeout=30,
    )

    print("Status:", response.status_code)
    print("Body:", response.text)

    response.raise_for_status()

    print("✅ Invoice email sent successfully.")