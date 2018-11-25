import datetime, json, sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from lib.models.Monitoring import MonitoringModel
from lib import app
from lib.config import SLACK_WEBHOOK_URL
import requests


def main():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(hours=1)
    print('='*20, 'BATCH START', '='*20)
    print('='*20, 'START DATE: {}'.format(start_date), '='*20)
    print('='*20, 'END DATE: {}'.format(end_date), '='*20)
    with app.app_context():
        monitoring_db = MonitoringModel()
        dead_user = monitoring_db.check_dead_user(start_date, end_date)

        ## TODO slackに通知を送る
        if len(dead_user) != 0:
            text = u"DEAD USER DETECTED!!! \n```\n {} \n```".format(dead_user)
        else:
            text = u'NO USER IS DEAD'
        print(text)
        payload = {
            "channel": "@marutaku",
            "username": "webhookbot",
            "text": text,
            "icon_emoji": ":ghost:"

        }
        print(SLACK_WEBHOOK_URL)
        response = requests.post(SLACK_WEBHOOK_URL,
                                 json=payload)


if __name__ == '__main__':
    main()
