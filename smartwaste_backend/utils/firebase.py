from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging

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
    return messaging.send(message)