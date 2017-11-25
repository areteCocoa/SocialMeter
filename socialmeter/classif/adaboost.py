# adaboost.py

from ..chain_links import Module


class AdaBoostModule(Module):
    """
    The AdaBoostModule uses the AdaBoost ensemble classifier
    in conjunction with other classifier modules.
    """
    def __init__(self):
        self.classifier = None  # TODO
        self.keys = list()
