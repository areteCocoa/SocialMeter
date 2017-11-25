# base.py
#
# This file defines many of the base classes for classifier
# modules.
#
# If you are looking to define an sklearn classifier or ensemble,
# you may look into subclassing the SKLearnClassifierModule first.
# If that does not fit your needs, subclassing the ClassifierModule
# provides some convenience functionality.

from ..chain_links import Module


class ClassifierModule(Module):
    """
    The ClassifierModule defines some common functionality
    among classifier modules.
    """
    def __init__(self):
        self.classifier = None
        self.keys = list()

    def train(self, preclass_link, training_data):
        """
        The train method should be used to train the
        classifier.

        The only shared code between all classifiers is the
        convenience method of calling set_keys.
        """
        self.set_keys(preclass_link)

    def set_keys(self, preclass_link):
        """
        Set keys takes the preclassifier link and retrieves
        all the keys from it, then sets self.keys to the
        list of keys.
        """
        keys = list()
        for mod in preclass_link.mods:
            keys.append(mod.key)
        self.keys = keys

    def features_for_data(self, data):
        features_dict = dict()
        for key in self.keys:
            features_dict[key] = data[key]

        features = list()
        for v in features_dict.values():
            features.append(v)
        return features


class SKLearnClassifierModule(ClassifierModule):
    """
    SKLearnClassifierModule defines some common functionality
    for sklearn's classifiers.
    """
    def __init__(self):
        super().__init__()

    def train(self, preclass_link, training_data):
        """
        This override of train calls .fit on the classifier. We
        make the assumption that all sklearn classifiers will
        use the .fit method to train their classifiers.

        Note that because there is no check on self.classifier,
        the classifier MUST be set before calling train. The
        best method for doing this is with a subclass that
        imports the appropriate sklearn class and sets it in
        the __init__ method.
        """
        super().train(preclass_link, training_data)
        self.classifier.fit(training_data[0], training_data[1])

    def process(self, data):
        features = self.features_for_data(data)
        p = self.classifier.predict([features])
        data["classification"] = p
        return super().process(data)
