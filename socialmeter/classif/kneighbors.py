# kneighbors.py

from .base import SKLearnClassifierModule

from sklearn.neighbors import KNeighborsClassifier


class KNeighborsModule(SKLearnClassifierModule):
    def __init__(self):
        super().__init__()
        self.classifier = KNeighborsClassifier()
