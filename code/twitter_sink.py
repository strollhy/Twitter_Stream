import sys
import threading
import time

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


class TwitterSink:
    """ Twitter stream sink that hosts multiple streams
    """
    def __init__(self, tags):
        self.streams = []
        for tag in tags:
            self.streams.append(TwitterStream(tag, tags[0]))
            self.streams[-1].start()

    def start_query(self):
        """ Start query on each twitter stream

        will wait till all stream have new updates
        """
        s1, s2 = None, None

        while 1:
            s_1, s_2 = [s.cache for s in self.streams]

            # if there is update
            if s_1 == s1 or s_2 == s2:
                time.sleep(2)
                continue

            s1, s2 = s_1, s_2
            print s1
            print s2
            print


class TwitterStream(threading.Thread):
    """ Twitter stream class
    """
    def __init__(self, tag, correct_tag):
        super(TwitterStream, self).__init__()
        self.tag = tag
        self.correct_tag = correct_tag
        self.cache = None

    def run(self):
        l = StdOutListener(self)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = Stream(auth, l)
        stream.filter(track=[self.tag], languages=['en'])


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__(self, host):
        self.host = host

    def on_data(self, data):
        tweet = GetTweets.get(data)
        if not tweet:
            return

        keywords = GetKeywords.get(tweet, self.host.tag)
        if not keywords['words']:
            return

        if self.host.tag == self.host.correct_tag:
            keywords["label"] = 1
        else:
            keywords["label"] = 0

        self.host.cache = keywords

    def on_error(self, status):
        print status


if __name__ == '__main__':

    if len(sys.argv) <= 2:
        exit()

    sink = TwitterSink(sys.argv[1:])
    sink.start_query()