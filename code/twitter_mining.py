import time

from winnow import *
from twitter_sink import TwitterSink


c = 0.97
f = open("../data/out.csv", "w")
f.close()


class Measure:
    def __init__(self):
        self.fp = 0
        self.tp = 0
        self.fn = 0
        self.tn = 0

    def eval(self, tup, label):

        fact = tup["label"]

        # Evalutation
        self.fp *= c
        self.tp *= c
        self.fn *= c
        self.tn *= c

        if label > fact:
            self.fp += 1

        elif label < fact:
            self.fn += 1

        elif label == 1:
            self.tp += 1

        else:
            self.tn += 1

        acc = (self.tp + self.tn)/(self.tp + self.fn + self.tn + self.fp + .1)
        pre = self.tp / (self.tp + self.fp + .1)
        rec = self.tp / (self.tp + self.fn + .1)

        acc = int(acc * 100) / 100.0
        pre = int(pre * 100) / 100.0
        rec = int(rec * 100) / 100.0

        print tup["text"]
        print tup["words"]
        # print [winnow.stack[word][0] for word in tup["words"] if word in winnow.stack]
        print ">>>> Get %s but actually is %s" % (label, fact)
        print ">>>> Accuracy: %s,\t Precision: %s,\t Recall: %s" % (acc, pre, rec)
        # print ">>>> List length: %s" % len(winnow.stack)
        print

        out = "%s,%s,%s\n" % (acc, pre, rec)
        f = open("../data/out.csv", "a")
        f.write(out)
        f.close()


def train(tup, winnow):
    winnow.add(tup['words'])
    label = winnow.predict(tup['words'])
    winnow.learn(label, tup)
    return label


if __name__ == '__main__':
    sink = TwitterSink(["#tech", "#life", "phone"])

    winnow = [BalancedWinnow(), AccumuWinnow()]
    measure = Measure()

    s1, s2, s000 = None, None, None

    while 1:
        # query each stream
        s_1, s_2, s_000 = sink.stream.cache

        # if s_000 and winnow.predict(s_000["words"]):
        #     print "Tech tweets found:", s_000["text"]

        # if there is update
        if s_1 == s1 or s_2 == s2:
            time.sleep(1)
            continue

        s1, s2 = s_1, s_2
        labels = [train(s1, winnow[0]), train(s1, winnow[1]), s1["label"]]
        print "=========", labels
        label = labels[0] and labels[1]
        # label = train(s1, winnow[0])
        measure.eval(s1, label)

        labels = [train(s2, winnow[0]), train(s2, winnow[1]), s2["label"]]
        print "=========", labels
        label = labels[0] and labels[1]

        # label = train(s1, winnow[0])
        measure.eval(s2, label)


