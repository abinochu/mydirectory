import math


class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.proba = dict()
        self.classes = set()


    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        dictt = {}
        unique_class = set(y)
        self.classes = unique_class
        for i in unique_class:
            dictt[i] = []
        for k in range(len(X)):
            dictt[y[k]].extend(X[k])
        unique_words = set()
        for i in range(len(X)):
            u = set(X[i])
            unique_words.update(u)
        table = {}
        for word in unique_words:
            table[word] = {}
            for g in unique_class:
                table[word][g] = dictt[g].count(word)
        self.proba = table
            

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predictions = []
        for x in X:
            xproba = {}
            for i in self.classes:
                xproba[i] = 0
            for xword in x:
                if xword in self.proba:
                    for itm in self.classes:
                        xproba[itm] += math.log2((self.proba[xword][itm] + self.alpha) / (sum(list(self.proba[xword].values())) + (self.alpha * len(self.proba))))
            max_k = None
            max_val = float('-inf')
            for key, value in xproba.items():
                if value > max_val:
                    max_val = value
                    max_k = key
            predictions.append(max_k)
        return predictions

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        predictions = self.predict(X_test)
        matchs = 0
        for ts in range(len(y_test)):
            if y_test[ts] == predictions[ts]:
                matchs += 1
        return matchs / len(y_test) * 100