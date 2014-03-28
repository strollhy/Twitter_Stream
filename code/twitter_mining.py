import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from extract_tweets import GetTweets
from extract_keywords import GetKeywords
from winnow import *

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="H67uY9pyjvuxWj4jQIUvA"
consumer_secret="2xZ3h1YKMspzApq9oy1yL4O6u3plNuFmXmBWbHx8"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="391111024-iUGWoFcYHfm0oyyWv7O0byZMcWFTenQyARMe2m0Z"
access_token_secret="BQfZYNGTgWqxyZAb26SruzT5KjFAyhyeISjcmYL0Qd1KJ"

c = 0.97


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__(self, winnow):
        self.winnow = winnow

        self.tp = 0.0
        self.fp = 0.0
        self.tn = 0.0
        self.fn = 0.0

    def on_data(self, data):
        tweet = GetTweets.get(data)
        if not tweet:
            return

        keywords = GetKeywords.get(tweet, sys.argv[1])
        if not keywords["words"]:
            return

        print keywords

        # winnow
        self.winnow.add(keywords['words'])
        label = self.winnow.predict(keywords['words'])
        self.winnow.learn(label, keywords)

        # Evalutation
        fact = keywords['label']
        self.fp *= c
        self.tp *= c
        self.fn *= c
        self.tn *= c

        if label > fact:
            self.fp += 1

        elif label < fact:
            self.tn += 1

        elif label == 1:
            self.tp += 1

        else:
            self.fn += 1

        acc = (self.tp + self.fn)/(self.tp + self.fn + self.tn + self.fp + 1)
        pre = self.tp / (self.tp + self.fp + 1)
        rec = self.tp / (self.tp + self.fn + 1)

        acc = int(acc * 100) / 100.0
        pre = int(pre * 100) / 100.0
        rec = int(rec * 100) / 100.0
        print ">>>> Get %s but actually was %s" % (label, fact)
        print ">>>> Accuracy: %s,\t Precision: %s,\t Recall: %s" % (acc, pre, rec)
        print ">>>> List length: %s" % len(self.winnow.stack)

    def on_error(self, status):
        print status


## main
def main():
    if len(sys.argv) == 1:
        exit()

    window = BalancedWinnow(1000)

    l = StdOutListener(window)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=sys.argv[1:], languages=['en'])

if __name__ == '__main__':
    main()