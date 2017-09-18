# chain-links.py

import nltk
from sklearn.naive_bayes import GaussianNB


DEBUG = True


def dlog(s):
    if DEBUG is True:
        print(s)


INPUT_MOD = "input-module"
PRECLASS_MOD = "preclass-module"
CLASS_MOD = "class-module"
OUTPUT_MOD = "output-module"

INPUT_LINK = "input-link"
PRECLASS_LINK = "pre-classification-link"
CLASS_LINK = "classification-link"
OUTPUT_LINK = "output-link"


# MODULES
class Module:
    def set_mod_type(self, mod_type):
        self.mod_type = mod_type

    def process(self, data):
        self.handler(self, data)

    def set_handler(self, handler):
        self.handler = handler

    def set_id(self, new_id):
        self.identifier = new_id

    def set_column_format(self, c_format):
        self.__column_format = c_format[:]
        dlog("Set column format for Module {} to {}.".format(self, c_format))

    def column_format(self):
        return self.__column_format


# TODO: Implement a general FEModule that takes a FE class and
# uses it to extract the features
# class FeatureExtractorModule(Module):
#     def __init__(self, extractor_class):
#         self.extractor_class = extractor_class

#     def process(self, data):
#         if "text" in data.keys():
#             text = data["text"]


class AdjectiveCountModule(Module):
    def __init__(self):
        self.set_mod_type(PRECLASS_MOD)
        self.feature_extractor = AdjectiveCounterFE

    def process(self, data):
        if "text" in data.keys():
            text = data["text"]
            data["features"]["adj-count"] = AdjectiveCounterFE.extract(text)
        super().process(data)


class AdjectiveCounterFE():
    def extract(text):
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        adj_count = 0
        for word, tag in pos_tags:
            if tag[0:2] == "JJ":
                adj_count += 1
        return adj_count


class NBClassifierModule(Module):
    def __init__(self):
        self.set_mod_type(CLASS_MOD)
        self.classifier = GaussianNB()

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
        features_dict = data["features"]
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


class OutputModule(Module):
    def __init__(self):
        self.set_mod_type(OUTPUT_MOD)

    def process(self, data):
        # Convert dataframe to dict
        d = data.to_dict()

        # If we don't have text
        if "text" not in d.keys():
            d["text"] = "(text not found)"

        super().process(d)


# LINKS
class Link:
    def __init__(self, owner, link_type):
        self.owner = owner
        self.link_type = link_type
        self.mods = list()
        self.column_format = None
        dlog("Finished initializing Link {}.".format(self))

    def add_mod(self, mod):
        self.mods.append(mod)
        mod.set_handler(self.handle_mod_data)
        mod.set_id(len(self.mods))
        if self.column_format is not None:
            mod.set_column_format(self.column_format)

    def process(self, data):
        self.mods[0].process(data)

    def handle_mod_data(self, sender, data):
        if sender.identifier == len(self.mods):
            # Finished all the modules in the link, time to pass up to
            # the chain
            self.handler(self, data)
        else:
            self.mods[sender.identifier].process(data)

    def set_handler(self, handler):
        self.handler = handler

    def set_column_format(self, c_format):
        self.column_format = c_format[:]
        dlog("Set column format for link {} to {}.".format(self, c_format))
        for m in self.mods:
            m.set_column_format(self.column_format)

    def is_empty(self):
        return len(self.mods) == 0


# CHAINS
class Chain:
    def __init__(self):
        self.input_link = Link(self, INPUT_LINK)
        self.input_link.set_handler(self.link_finished)

        self.preclass_link = Link(self, PRECLASS_LINK)
        self.preclass_link.set_handler(self.link_finished)

        self.class_link = Link(self, CLASS_LINK)
        self.class_link.set_handler(self.link_finished)

        self.output_link = Link(self, OUTPUT_LINK)
        self.output_link.set_handler(self.link_finished)

        dlog("Finished initializing chain {}.".format(self))

    def set_handler(self, handler):
        self.handler = handler

    def set_column_format(self, c_format):
        self.column_format = c_format

        self.input_link.set_column_format(c_format)
        self.preclass_link.set_column_format(c_format)
        self.class_link.set_column_format(c_format)
        self.output_link.set_column_format(c_format)

    def add_mod(self, mod):
        mod_type = mod.mod_type
        if mod_type == INPUT_MOD:
            self.input_link.add_mod(mod)
        elif mod_type == PRECLASS_MOD:
            self.preclass_link.add_mod(mod)
        elif mod_type == CLASS_MOD:
            self.class_link.add_mod(mod)
        elif mod_type == OUTPUT_MOD:
            self.output_link.add_mod(mod)

    def start_if_ready(self):
        if not self.input_link.is_empty()\
           and not self.preclass_link.is_empty()\
           and not self.class_link.is_empty()\
           and not self.output_link.is_empty():
            self.input_link.mods[0].start()
        else:
            if self.input_link.is_empty():
                print("Not ready to start, input link is empty.")
            if self.preclass_link.is_empty():
                print("Not ready to start, preclass link is empty.")
            if self.class_link.is_empty():
                print("Not ready to start, class link is empty.")
            if self.output_link.is_empty():
                print("Not ready to start, output link is empty.")

    def link_finished(self, sender, data):
        if sender.link_type == INPUT_LINK:
            data["features"] = dict()
            self.preclass_link.process(data)
        elif sender.link_type == PRECLASS_LINK:
            self.class_link.process(data)
        elif sender.link_type == CLASS_LINK:
            self.output_link.process(data)
        else:
            self.handler(data)
