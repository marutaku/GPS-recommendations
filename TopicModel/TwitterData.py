import twitter
import config

class TwitterData(object):
    def __init__(self):
        self.api = twitter.Api(
            consumer_key=config.TWITTER_CONSUMER_KEY,
            consumer_secret=config.TWITTER_CONSUMER_SECRET,
            access_token_key=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACEESS_SECRET
        )

    def get_verify_credentials(self):
        return self.api.VerifyCredentials()

    def get_home_time_line(self):
        response = self.api.GetHomeTimeline(count=200)
        tl = self._parse_tweet_array(response)
        return tl

    def get_user_tweet(self,screen_name=None, count=200):
        response = self.api.GetUserTimeline(screen_name=screen_name, count=count)
        return self._parse_tweet_array(response)



    def _parse_tweet_array(self, tweets):
        tl = []
        for tweet in tweets:
            user = tweet.user.name
            text = tweet.text
            tl.append('{0}:  {1}'.format(user, text))
        return tl




if __name__ == '__main__':
    app = TwitterData()
    # print(app.get_verify_credentials())
    # for i in app.get_home_time_line():
    #     print(i)

    for i in app.get_user_tweet('he_ta_reeee'):
        print(i)





