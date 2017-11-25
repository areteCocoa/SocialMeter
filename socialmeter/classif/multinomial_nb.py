# multinomial_nb.py

from ..chain_links import Module

from sklearn.naive_bayes import MultinomialNB


class MultinomialNBModule(Module):
    """
    A module wrapper around the sklearn Multinomial Naive
    Bayes classifier. More information about it can be found here:
    http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html#sklearn.naive_bayes.MultinomialNB
    """
    def __init__(self):
        self.classifier = MultinomialNB()
        self.keys = list()

    def train(self, preclass_link, training_data):
        features = training_data[0]
        classifications = training_data[1]
        for mod in preclass_link.mods:
            self.keys.append(mod.key)
        self.classifier.fit(features, classifications)

    def process(self, data):
        features_dict = dict()
        for key in self.keys:
            features_dict[key] = data[key]

        features = list()
        for v in features_dict.values():
            features.append(v)
        p = self.classifier.predict([features])
        if p == '0':
            data["classification"] = "negative"
        else:
            data["classification"] = "positive"
        return super().process(data)
