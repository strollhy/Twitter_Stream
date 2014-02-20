import re

class GetKeywords:

	def __init__(self):
		pass

	@staticmethod
	def get(tweet):
		tweet = re.sub("http://.+? ", "", tweet)
		tweet = re.sub("#[a-zA-Z]+","", tweet)
		return re.findall("[a-zA-Z]+", tweet)

	def test(self, tag):
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
	GetKeywords().test('tech')