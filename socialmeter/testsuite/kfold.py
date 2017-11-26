# test.kfold.py

from sklearn.model_selection import cross_val_score
import numpy as np


class ValidationTest():
    def __init__(self):
        pass

    def test_meter(self, meter, data):
        """
        Tests the meter for accuracy and returns the (percentage,
        std-dev).

        Subclasses should not call this methid, it is only here
        to server as documentation for how a subclass should be
        implemented.

        The meter should contain an untrained classifier, and
        data should be the data that you would have used to train
        it.
        """
        return None

    def test_meters(self, meters, data):
        """
        Tests the list of meters for accuracy and then returns
        them in a sorted order.

        Similar to above, this is not implemented and should not
        be called, and is only included to serve as documentation
        for subclassing.
        """
        results = list()
        for m in meters:
            r = self.test_meter(m, data)
            results.append((m, r))
        return sorted(results, key=lambda r: r[1][0])


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

    def test_meter(self, meter, data):
        texts = data[0]
        sentiments = data[1]

        # Extract the features using the meter's built in function
        # extract_features.
        features = list()
        for t in texts:
            t_features = np.asarray(meter.extract_single_features(t))
            features.append(t_features)
        features = np.asarray(features)

        print("KFoldValidationTest finished extracting features from \
test data.")


        # Run the cross validation on the chain
        classifier = meter.class_mod.classifier
        scores = cross_val_score(classifier, features,
                                 sentiments, cv=self.n_folds)

        print("Finished cross validation.")

        mean = scores.mean()
        std_dev = scores.std()

        return (mean, std_dev)
