from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders

from io import BytesIO
import base64

from xhtml2pdf import pisa

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from .models import Order


def send_invoice_email(order_id):

    order = Order.objects.prefetch_related("items__product").get(id=order_id)

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

    configuration = sib_api_v3_sdk.Configuration()

    configuration.api_key["api-key"] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email = sib_api_v3_sdk.SendSmtpEmail(

        sender={
            "name": "Smart Shop",
            "email": "smartshop.notify@gmail.com"
        },

        to=[
            {
                "email": order.user.email
            }
        ],

        subject=f"Invoice - Order #{order.id}",

        html_content="""
        <h2>Invoice Attached</h2>

        <p>Thank you for shopping with Smart Shop.</p>

        <p>Your invoice is attached as a PDF.</p>
        """,

        attachment=[
            {
                "name": f"invoice_{order.id}.pdf",
                "content": pdf_base64
            }
        ]
    )

    try:
        api_instance.send_transac_email(email)
        print("Invoice email sent successfully.")

    except ApiException as e:
        print("Brevo API Error:", e)
        raise