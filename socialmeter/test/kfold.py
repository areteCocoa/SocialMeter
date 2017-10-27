# test.kfold.py

from sklearn.model_selection import cross_val_score


class ValidationTest():
    def __init__(self):
        pass

    def test_chain(self, chain, data):
        """
        Tests the chain for accuracy and returns the percentage.
        Subclasses should not call this method, it is only here
        to serve as documentation for how a subclass should be
        implemented.

        The chain should contain an untrained classifier, and data
        should be the data that you would use to train it.

        data should be a list of tuples of (text, sentiment)
        """
        return None

    def test_chains(self, chains, data):
        return None


class KFoldValidationTest(ValidationTest):
    """
    KFoldValidationTest is a test that uses K-fold to test
    a chain.

    Uses sklearn's cross_val_score function to get the score.

    The number of folds can be set using .set_n_folds(n).
    """
    def __init__(self):
        super().__init__()
        self.n_folds = 5

    def set_n_folds(self, n):
        self.n_folds = n

    def prep_chain():
        pass

    def test_chain(self, chain, data):
        # Get the mods
        class_mod = chain.class_link.mods[0]
        
        texts = data[0]
        sentiments = data[1]

        # Extract the features using the chain's preclass
        # link's mod's feature extractors (there has to be
        # an easier way to do this...
        features = list()
        for t in texts:
            t_feature = list()
            for mod in chain.preclass_link.mods:
                fe = mod.feature_extractor
                feature = fe.extract(t)
                t_feature.append(feature)
            features.append(t_feature)

        # Run the cross validation on the chain
        classifier = class_mod.classifier
        scores = cross_val_score(classifier, features,
                                 sentiments, cv=self.n_folds)
        print("Testing {}.".format(hex(id(classifier))))

        mean = scores.mean()
        error_margin = scores.std() * 2

        return (mean, error_margin)

    def test_chains(self, chains, data):
        results = list()
        for c in chains:
            r = self.test_chain(c, data)
            results.append((c, r))
        return sorted(results, key=lambda r: r[1][0])
