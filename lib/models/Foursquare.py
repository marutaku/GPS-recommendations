import requests
from urllib.parse import urljoin
class Foursquare(object):

    BASE_URL = 'https://api.foursquare.com/v2/venues'

    def  __init__(self):
        pass

    def search_place(self, latitude, longitude):
        url = urljoin(self.BASE_URL, 'search')
        location = '{lat},{long}'.format(lat=latitude, long=longitude)

        params = dict(
            ll=location,
            radius=100,
            limit=5
        )
        try:
            requests.post(url, data=params).json()
        except requests.exceptions.HTTPError as e:
            print(e)
