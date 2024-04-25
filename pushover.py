import requests
import time
class PushoverHandler:
    def __init__(self, api_token, user_key, time_enabled=False):
        self.api_token = api_token
        self.user_key = user_key
        self.url = "https://api.pushover.net/1/messages.json"
        self.time_enabled = time_enabled
    def send_notification(self, message, title=None, sound=None, priority=None, url=None, url_title=None):
        """
        Send a notification to the user's devices.
        
        Parameters:
            message (str): The message content of the notification.
            title (str, optional): The title of your message.
            sound (str, optional): The name of one of the sounds supported by device clients to override the user's default sound choice.
            priority (int, optional): Defines how messages are displayed on devices (-2 to 2).
            url (str, optional): A supplementary URL to show with your message.
            url_title (str, optional): A title for your supplementary URL, otherwise just the URL is shown.
        """
        if self.time_enabled:
            ##Add time date to message
            message = message + " @ " + time.strftime("%Y-%m-%d %H:%M:%S")
        payload = {
            "token": self.api_token,
            "user": self.user_key,
            "message": "🐦🦆🦅! " + message,
            "title": title,
            "sound": sound,
            "priority": priority,
            "url": url,
            "url_title": url_title
        }
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(self.url, data=payload)
        if response.status_code != 200:
            print(f"Failed to send notification: {response.text}")


        return response.json()
