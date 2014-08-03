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
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""


class TwitterSink:
    """ Twitter stream sink that hosts multiple streams
    """
    def __init__(self, tags):
        self.stream = TwitterStream(tags)
        self.stream.start()

    def start_query(self):
        """ Start query on each twitter stream

        will wait till all stream have new updates
        """
        s1, s2 = None, None

        while 1:
            s_1, s_2 = self.stream.cache

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
    def __init__(self, tags):
        super(TwitterStream, self).__init__()
        self.daemon = True
        self.tags = tags
        self.correct_tag = tags[0]
        self.cache = [None] * len(tags)
        self.getKeywords = GetKeywords()

    def run(self):
        l = StdOutListener(self)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = Stream(auth, l)
        stream.filter(track=self.tags, languages=['en'])


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

        tag = self.host.tags[0]
        indx = 0
        for t in self.host.tags:
            if t in tweet:
                tag = t
                break
            indx += 1
        indx = min(indx, len(self.host.tags)-1)


        keywords = self.host.getKeywords.get(tweet, tag)
        if not keywords['words']:
            return

        if tag == self.host.correct_tag:
            keywords["label"] = 1
        else:
            keywords["label"] = 0

        try:
            self.host.cache[indx] = keywords
        except:
            pass

    def on_error(self, status):
        print status


if __name__ == '__main__':

    if len(sys.argv) <= 2:
        exit()

    sink = TwitterSink(sys.argv[1:])
    sink.start_query()
