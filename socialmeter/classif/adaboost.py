# adaboost.py

from .base import SKLearnClassifierModule

from sklearn.ensemble import AdaBoostClassifier


class AdaBoostModule(SKLearnClassifierModule):
    """
    The AdaBoostModule uses the AdaBoost ensemble classifier
    in conjunction with other classifier modules.

    Note: the module is initialized with a DecisionTreeClassifier
    by default.
    """
    def __init__(self):
        super().__init__()
        self.classifier = AdaBoostClassifier()
