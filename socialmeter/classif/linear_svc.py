# linear_svc.py

from .base import SKLearnClassifierModule

from sklearn.svm import LinearSVC


class LinearSVCModule(SKLearnClassifierModule):
    def __init__(self):
        super().__init__()
        self.classifier = LinearSVC()
