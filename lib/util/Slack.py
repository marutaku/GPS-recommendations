import requests
from lib.config import SLACK_WEBHOOK_URL


class SlackUtil(object):
    @staticmethod
    def post_slack(user, text):
        payload = {
            "channel": user,
            "username": "webhookbot",
            "text": text,
            "icon_emoji": ":ghost:"

        }
        requests.post(SLACK_WEBHOOK_URL, json=payload)
        return

