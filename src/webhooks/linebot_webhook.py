from flask import current_app
from linebot.models import TextMessage
from linebot.v3.webhook import MessageEvent
from middlewares.webhook.webhook_factory import WebHookFactoy

webhook_handler = current_app.linebot.handler

class LinebotWebHook:
    
    @classmethod
    def _validate_type(type):
        
    @webhook_handler.add(MessageEvent, message=TextMessage)
    @staticmethod
    def handle_message(event):
        """ 
            "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "id": "14353798921116",
                    "text": "Hello, world"
                },
                "timestamp": 1625665242211,
                "source": {
                    "type": "user",
                    "userId": "U80696558e1aa831..."
                },
                "replyToken": "757913772c4646b784d4b7ce46d12671",
                "mode": "active",
                "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                "deliveryContext": {
                "isRedelivery": false
                }
            },
            ]
        """
        reply_token= event.reply_token
        message = event.message
        WebHookFactoy
