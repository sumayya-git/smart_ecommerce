import base64
import requests
from django.conf import settings


BREVO_URL = "https://api.brevo.com/v3/smtp/email"


def send_brevo_email(
    to_email,
    subject,
    html_content,
    attachments=None,
):

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": "Smart Shop",
            "email": "smartshop.notify@gmail.com",
        },
        "to": [
            {
                "email": to_email,
            }
        ],
        "subject": subject,
        "htmlContent": html_content,
    }

    if attachments:
        payload["attachment"] = attachments

    response = requests.post(
        BREVO_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()

    return response.json()


def create_pdf_attachment(filename, pdf_bytes):

    return {
        "name": filename,
        "content": base64.b64encode(pdf_bytes).decode("utf-8"),
    }