from flask import request

from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage


class LineBotService:

    def __init__(self, access_token, secret):
        self.linebot = LineBotApi(access_token)
        self.handler = WebhookHandler

