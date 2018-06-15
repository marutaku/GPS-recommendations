import twitter
import config

class Twitter(object):
    def __init__(self):
        self.api = twitter.api(
            consumer_key=config.TWITTER_CONSUMER_KEY,
            consumer_secret=config.TWITTER_CONSUMER_SECRET,
            access_token_key=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACEESS_SECRET
        )

    def get_verify_credentials(self):
        return self.api.VerifyCredentials()



if __name__ == '__main__':
    Twitter().get_verify_credentials()



