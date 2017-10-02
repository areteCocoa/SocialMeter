# test.kfold.py

from sklearn.model_selection import cross_val_score


class ValidationTest():
    def __init__(self):
        pass

    # Tests the chain for accuracy and returns the percentage.
    # Subclasses should not call this method, it is only here
    # to serve as documentation for how a subclass should be
    # implemented.
    #
    # The chain should contain an untrained classifier, and data
    # should be the data that you would use to train it.
    #
    # data should be a list of tuples of (text, sentiment)
    def test_chain(self, chain, data):
        return 0


# KFoldValidationTest is a test that uses K-fold to test
# a chain.
#
# The number of folds can be set using .set_n_folds(n).
class KFoldValidationTest(ValidationTest):
    def __init__(self):
        super().__init__()
        self.n_folds = 5

    def set_n_folds(self, n):
        self.n_folds = n

    def prep_chain():
        pass

    # K-Fold validation uses sklearn's cross_val_score
    # function to score it.
    def test_chain(self, chain, data):
        # Get the mods
        class_mod = chain.class_link.mods[0]

        features = data[0]
        classifs = data[1]

        # Run the cross validation on the chain
        classifier = class_mod.classifier
        scores = cross_val_score(classifier, features,
                                 classifs, cv=self.n_folds)

        mean = scores.mean()
        error_margin = scores.std() * 2

        return (mean, error_margin)
