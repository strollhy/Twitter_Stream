""" Balanced Winnow


"""
learning_rate = 2.0


class BalancedWinnow:
    def __init__(self, size):
        self.window_size = size
        self.stack = {}

    def add(self, words):
        for word in words:
            if word not in self.stack:
                self.stack[word] = 0.5

    def predict(self, words):
        s = sum([self.stack[word] for word in words])
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

                self.stack[word] /= learning_rate

                # if weight is too small, delete the word
                if self.stack[word] < 0.001:    # 1/2^10
                    del self.stack[word]

        # if true-negative, raise up the weight
        else:
            for word in keywords['words']:
                self.stack[word] *= learning_rate

def main():
    pass

if __name__ == '__main__':
    main()