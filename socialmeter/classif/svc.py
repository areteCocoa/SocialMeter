# svc.py

from .base import SKLearnClassifierModule

from sklearn.svm import SVC


class SVCModule(SKLearnClassifierModule):
    def __init__(self):
        super().__init__()
        self.classifier = SVC()
