import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from extract_tweets import GetTweets
from extract_keywords import GetKeywords

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="H67uY9pyjvuxWj4jQIUvA"
consumer_secret="2xZ3h1YKMspzApq9oy1yL4O6u3plNuFmXmBWbHx8"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="391111024-iUGWoFcYHfm0oyyWv7O0byZMcWFTenQyARMe2m0Z"
access_token_secret="BQfZYNGTgWqxyZAb26SruzT5KjFAyhyeISjcmYL0Qd1KJ"


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__(self):
        pass

    def on_data(self, data):
    	tweet =  GetTweets.get(data)
        if not tweet:
            return

        print tweet
        keywords = GetKeywords.get(tweet, sys.argv[1])
        print keywords

    def on_error(self, status):
        print status


if __name__ == '__main__':

    if len(sys.argv) <= 2:
        exit()

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=[sys.argv[1], sys.argv[2]], languages=['en'])
    