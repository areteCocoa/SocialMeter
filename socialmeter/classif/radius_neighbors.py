# radius_neighbors.py

from .base import SKLearnClassifierModule

from sklearn.neighbors import RadiusNeighborsClassifier


class RadiusNeighborsModule(SKLearnClassifierModule):
    def __init__(self):
        super().__init__()
        self.classifier = RadiusNeighborsClassifier()
