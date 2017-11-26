# neural_net.py

from .base import SKLearnClassifierModule

from sklearn.neural_network import MLPClassifier


class MLPModule(SKLearnClassifierModule):
    def __init__(self):
        super().__init__()
        self.classifier = MLPClassifier()
