import requests
from urllib.parse import urljoin
from lib.config import FOURSQUARE_SECRET, FOURSQUARE_CLIENT_ID
import datetime
class Foursquare(object):

    def  __init__(self):
        self.BASE_URL = 'https://api.foursquare.com/v2/venues/'


    def search_place(self, latitude, longitude):
        url = urljoin(self.BASE_URL, 'search')
        location = '{lat},{long}'.format(lat=latitude, long=longitude)
        now = datetime.datetime.now()
        params = dict(
            ll=location,
            radius=100,
            limit=5,
            v=now.strftime('%Y%m%d'),
            client_id=FOURSQUARE_CLIENT_ID,
            client_secret=FOURSQUARE_SECRET
        )
        try:
            req = requests.get(url, params=params)
            result = req.json()
            return result
        except requests.exceptions.HTTPError as e:
            print(e)
