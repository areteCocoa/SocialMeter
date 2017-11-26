# nu_svc.py

from .base import SKLearnClassifierModule

from sklearn.svm import NuSVC


class NuSVCModule(SKLearnClassifierModule):
    def __init__(self):
        super().__init__()
        self.classifier = NuSVC()
