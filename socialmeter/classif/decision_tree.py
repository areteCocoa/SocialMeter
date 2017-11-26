# decision_tree.py

from .base import SKLearnClassifierModule

from sklearn.tree import DecisionTreeClassifier


class DecisionTreeModule(SKLearnClassifierModule):
    def __init__(self):
        super().__init__()
        self.classifier = DecisionTreeClassifier()
