""" Balanced Winnow


"""

class BalancedWinnow:
    """ Balanced Winnow

    Update weight by multiply
    """
    def __init__(self):
        self.stack = {}
        self.rate = 2.0

    def add(self, words):
        for word in words:
            if word not in self.stack:
                # set initial weights and count
                self.stack[word] = [0.5, 1]
            else:
                self.stack[word][1] += 1

    def predict(self, words):
        w = [self.stack[word][0] for word in words if word in self.stack]
        s = sum(w)
        if s > len(words)/2:
            return 1
        else:
            return 0

    def learn(self, label, keywords):
        fact = keywords['label']

        if label == fact:
            return

        # if false-positive, cut down the weight
        if label > fact:
            for word in keywords['words']:
                if word not in self.stack:
                    continue

                self.stack[word][0] /= self.rate

        # if true-negative, raise up the weight
        else:
            for word in keywords['words']:
                self.stack[word][0] *= self.rate

        # decay window 0.95^100 = 0.003
        for w in self.stack.keys():
            self.stack[w][1] *= 0.95
            if self.stack[w][1] < 0.001:
                print "=========== Remove word:", w
                del self.stack[w]


class AccumuWinnow():
    """ Accumulated Winnow

    Update weight by increasing
    """
    def __init__(self):
        self.stack = {}
        self.rate = 0.01

    def add(self, words):
        for word in words:
            if word not in self.stack:
                # set initial weights and count
                self.stack[word] = [0, 1]
            else:
                self.stack[word][1] += 1

    def predict(self, words):
        w = [self.stack[word][0] for word in words if word in self.stack]
        s = sum(w)
        if s > 0:
            return 1
        else:
            return 0

    def learn(self, label, keywords):
        fact = keywords['label']

        if label == fact:
            return

        # if false-positive, cut down the weight
        if label > fact:
            for word in keywords['words']:
                if word not in self.stack:
                    continue

                self.stack[word][0] -= self.rate

        # if true-negative, raise up the weight
        else:
            for word in keywords['words']:
                self.stack[word][0] += self.rate

        # decay window 0.95^100 = 0.003
        for w in self.stack.keys():
            self.stack[w][1] *= 0.95
            if self.stack[w][1] < 0.001:
                print "=========== Remove word:", w
                del self.stack[w]

def main():
    pass

if __name__ == '__main__':
    main()