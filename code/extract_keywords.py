import re

class GetKeywords:

    def __init__(self):
        # Load stop words
        self.stop = set([]) 

        f = open('../data/english.stop.txt')
        for line in f:
            self.stop.add(line.strip())

    def get(self, tweet, tag):
        text = tweet

        # remove urls
        tweet = re.sub("http://.+? ", "", tweet)
        tweet = re.sub("http://.+", "", tweet)
        tweet = re.sub("https://.+? ", "", tweet)
        tweet = re.sub("https://.+", "", tweet)

        # remove tag
        tweet = re.sub(tag, "", tweet)

        # remove RT
        tweet = re.sub("RT", "", tweet)
        tweet = re.sub("rt", "", tweet)

        # remove @somebody
        tweet = re.sub("@.+? ", "", tweet)

        # remove hash tags
        # tweet = re.sub("#.+","", tweet)

        keywords = [w for w in re.findall("[a-zA-Z]+", tweet) if w not in self.stop]
        return {'words': keywords, 'tag': tag, 'text': text}

def main(tag):
    f = open("../data/tweets.txt")
    out = open("../data/keywords.txt","w")
    out = open("../data/keywords.txt","a")

    words = {}

    for line in f:
        line = re.sub("http://.+? ", "", line)
        line = re.sub("#tech","", line)

        for word in re.findall("[a-zA-Z]+", line):
            if word in words:
                words[word] += 1
            else:
                words[word] = 1

    out.write(words.__str__())


if __name__ == '__main__':
    main('tech')