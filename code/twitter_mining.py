import time

from winnow import *
from twitter_sink import TwitterSink


c = 0.97
fp = 0
tp = 0
fn = 0
tn = 0

f = open("../data/out.csv", "w")
f.close()


def train(tup, winnow):
    winnow.add(tup['words'])
    label = winnow.predict(tup['words'])
    winnow.learn(label, tup)

    # Evalutation
    global fp, tp, fn, tn
    fact = tup["label"]

    fp *= c
    tp *= c
    fn *= c
    tn *= c

    if label > fact:
        fp += 1

    elif label < fact:
        tn += 1

    elif label == 1:
        tp += 1

    else:
        fn += 1

    acc = (tp + fn)/(tp + fn + tn + fp + 1)
    pre = tp / (tp + fp + 1)
    rec = tp / (tp + fn + 1)

    acc = int(acc * 100) / 100.0
    pre = int(pre * 100) / 100.0
    rec = int(rec * 100) / 100.0

    print tup["text"]
    print tup["words"]
    print ">>>> Get %s but actually is %s" % (label, fact)
    print ">>>> Accuracy: %s,\t Precision: %s,\t Recall: %s" % (acc, pre, rec)
    print ">>>> List length: %s" % len(winnow.stack)
    print

    out = "%s,%s,%s\n" % (acc, pre, rec)
    f = open("../data/out.csv", "a")
    f.write(out)
    f.close()


if __name__ == '__main__':
    sink = TwitterSink(["#tech", "#life", "phone"])
    winnow = BalancedWinnow(1000)

    s1, s2, s000 = None, None, None

    while 1:
        # query each stream
        s_1, s_2, s_000 = sink.stream.cache

        if s_000 and winnow.predict(s_000["words"]):
            print "Tech tweets found:", s_000["text"]

        # if there is update
        if s_1 == s1 or s_2 == s2:
            time.sleep(1)
            continue

        s1, s2 = s_1, s_2
        train(s1, winnow)
        train(s2, winnow)

