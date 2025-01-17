from firebase_admin import messaging

def send_fcm_notification(token, title, body):
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
       messaging.send(message)
    except Exception as e:
        # If there's an error, print the exception
        print(f"Failed to send notification: {e}")