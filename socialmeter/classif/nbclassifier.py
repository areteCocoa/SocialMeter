# classif.nbclassifier.py

from ..chain_links import Module, CLASS_MOD

from sklearn.naive_bayes import GaussianNB


class NBClassifierModule(Module):
    def __init__(self):
        self.set_mod_type(CLASS_MOD)
        self.classifier = GaussianNB()
        self.keys = []

    def train(self, preclass_link, training_data):
        features = training_data[0]
        classifications = training_data[1]
        for mod in preclass_link.mods:
            self.keys.append(mod.key)
        self.classifer = self.classifier.fit(features, classifications)

    def process(self, data):
        # Format the features so we can classify them
        features_dict = dict()
        for key in self.keys:
            features_dict[key] = data[key]

        features = list()
        for v in features_dict.values():
            features.append([v])
        p = self.classifier.predict(features)
        print("Predict: {}".format(p))
        if p == '0':
            data["classification"] = "negative"
        else:
            data["classification"] = "positive"
        super().process(data)
