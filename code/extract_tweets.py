import json

class GetTweets:

    def __init__(self):
        pass

    @staticmethod
    def get(content):
        content = json.loads(content)
        if "text" in content:
            return (content["text"].encode('ascii', 'ignore').lower()).strip()

    def test(self):
        f = open("../data/out.txt")
        out = open("../data/tweets.txt", "w")
        out = open("../data/tweets.txt", "a")

        for line in f:
            content = json.loads(line)
            if "lang" in content and content["lang"] == "en":
                out.write(content["text"].encode('ascii', 'ignore') + "\n\n")


if __name__ == '__main__':
    GetTweets().test()