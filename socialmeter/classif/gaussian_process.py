# gaussian_process.py

from .base import SKLearnClassifierModule

from sklearn.gaussian_process import GaussianProcessClassifier


class GaussianProcessModule(SKLearnClassifierModule):
    def __init__(self):
        super().__init__()
        self.classifier = GaussianProcessClassifier()
