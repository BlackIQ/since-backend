# Libs
import resend  # Resend
from enum import StrEnum

# Application
from core.settings import settings  # Settings

# Setup Resend
resend.api_key = settings.resend_apikey


# Emails (Senders)
class MailSender(StrEnum):
    INFO = "Since Info <info@since.amirhossein.info>"
    SECURITY = "Since Security <security@since.amirhossein.info>"
    SUPPORT = "Since Support <support@since.amirhossein.info>"


# send email util
def send_email(sender: str, to: str, subject: str, content: str):
    try:
        resend.Emails.send(
            {
                "from": sender,
                "to": to,
                "subject": subject,
                "html": content,
            }
        )
    except Exception as e:
        print(f"[MAIL ERROR] Failed to send email to {to}: {e}")
