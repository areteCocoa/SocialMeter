# classif.nbclassifier.py

from ..chain_links import Module

from sklearn.naive_bayes import GaussianNB


class NBClassifierModule(Module):
    """
    NBClassifierModule uses the GaussianNB classifier
    from sklearn. It is a module wrapper.
    """
    def __init__(self):
        self.classifier = GaussianNB()
        self.keys = []

    def train(self, preclass_link, training_data):
        features = training_data[0]
        classifications = training_data[1]
        for mod in preclass_link.mods:
            self.keys.append(mod.key)
        self.classifier.fit(features, classifications)

    def process(self, data):
        # Format the features so we can classify them
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
