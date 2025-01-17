from firebase_admin import messaging
import firebase_admin
from django.conf import settings
import os
def send_fcm_notification(token, title, body):
    service_key_path = "kanekt-89e07-firebase-adminsdk-fy4ac-11e5a32539.json"
    cred = firebase_admin.credentials.Certificate(service_key_path)
    firebase_admin.initialize_app(credential=cred)
    print(f"Notification sending with\nTitle: {title}\nBody: {body}\nToken: {token}")

    # Create the notification message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )
    print("Message created succesfully!")
    
    try:
        # Send the message to the specified token
       messaging.send_all([message])
    except Exception as e:
        # If there's an error, print the exception
        print(f"Failed to send notification: {e}")

send_fcm_notification(token="euz9d8x5Rjy6qHSyIP3E7R:APA91bFkJRfCx5LymEmOsIDPEmhYXngbuIotaO-34BnbduxUg5qCBABcxJx3NOkucx1Jr52RYeMnInWYKZFSa66Xaq6pwa9pzG9LEd5JuyEcLa_eXcMNAeQ", body="This is sent through a file", title="Test")