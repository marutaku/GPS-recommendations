import requests
from lib.config import SLACK_WEBHOOK_URL


class SlackUtil(object):
    @staticmethod
    def post_slack(user, text):
        print('='*30, 'REQUEST TO SLACK WEBHOOK', '='*30)
        payload = {
            "channel": user,
            "username": "webhookbot",
            "text": text,
            "icon_emoji": ":ghost:"
        }
        print(payload)
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        print('=' * 30, 'SLACK RESPONSE', '=' * 30)
        print(response.text)
        return

