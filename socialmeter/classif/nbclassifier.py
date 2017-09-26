# classif.nbclassifier.py

from ..chain_links import Module, CLASS_MOD

from sklearn.naive_bayes import GaussianNB


class NBClassifierModule(Module):
    def __init__(self):
        self.set_mod_type(CLASS_MOD)
        self.classifier = GaussianNB()
        self.keys = []

    def train(self, preclass_link, training_data):
        # Load the file, format the data to our specification
        # and train the classifier
        #
        # This is a temporary implementation of a long-term plan for
        # the framework architecture. Likely most of the functionality
        # except for the training will be moved to the user's responsibility.
        f = open(training_data, 'r')
        features = list()
        classifications = list()
        f.readline()  # Throwaway column line in the file

        # Store the feature extractor keys in the column to a list
        # for later so we know which keys to use
        for mod in preclass_link.mods:
            self.keys.append(mod.key)
        for i in range(1, 10):
            # Read in the file, run it through the feature identifiers and
            # store the features with the classifications.
            s = f.readline().split(',')
            sentiment = s[1]
            text = s[3].strip()

            # Run through the preclass chain
            classif = list()
            for mod in preclass_link.mods:
                fe = mod.feature_extractor
                classif.append(fe.extract(text))
            features.append(classif)
            classifications.append(sentiment)
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
