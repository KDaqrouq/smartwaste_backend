from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging
import logging

logger = logging.getLogger(__name__)

if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_FILE)
    firebase_admin.initialize_app(cred)

def send_push_v1(device_token:str, title:str, body:str):
    """Send FCM HTTP v1 push using Admin SDK."""
    message = messaging.Message(
        token=device_token,
        notification=messaging.Notification(
            title=title,
            body=body,
        )
    )
    try:
        response = messaging.send(message)
        logger.info(f"✅ Successfully sent push to {device_token[:12]}...: {response}")
        return response
    except Exception as e:
        logger.error(f"❌ Error sending push to {device_token[:12]}...: {e}", exc_info=True)
        raise