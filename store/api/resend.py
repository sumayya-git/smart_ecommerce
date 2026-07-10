import requests
from django.conf import settings


def send_resend_email(to_email, subject, html_content):
    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "from": "Smart Commerce <onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "html": html_content,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30,
        )

        response.raise_for_status()

        print("✅ Resend email sent successfully.")

        return response.json()

    except requests.exceptions.RequestException as e:
        print("❌ Resend Email Error:", e)
        raise