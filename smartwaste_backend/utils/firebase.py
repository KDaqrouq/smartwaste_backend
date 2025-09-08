from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging
import logging
from .firebase import *
import logging
from firebase_admin import messaging
from .firebase import *  # ensures Firebase app is initialized

# Set up logger (if not already set)
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout  # ensures logs appear in Render
    )

def send_push_v1(device_token: str, title: str, body: str, data: dict = None):
    """
    Send an FCM push notification via Firebase Admin SDK.

    Args:
        device_token (str): FCM device token
        title (str): Notification title
        body (str): Notification body
        data (dict, optional): Optional data payload
    Returns:
        dict: Contains success status and message_id or error info
    """
    message_kwargs = {"token": device_token}

    # Include notification payload
    if title or body:
        message_kwargs["notification"] = messaging.Notification(title=title, body=body)

    # Include optional data payload
    if data:
        message_kwargs["data"] = data

    message = messaging.Message(**message_kwargs)

    try:
        logger.info(f"📤 Sending push to {device_token[:12]}...")  # partial token for privacy
        response = messaging.send(message)
        logger.info(f"✅ Successfully sent push to {device_token[:12]}... | Message ID: {response}")
        return {"success": True, "message_id": response}
    except Exception as e:
        logger.error(f"❌ Error sending push to {device_token[:12]}...", exc_info=True)
        return {"success": False, "error": str(e)}