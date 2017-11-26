# multinomial_nb.py

from .base import SKLearnClassifierModule

from sklearn.naive_bayes import MultinomialNB


class MultinomialNBModule(SKLearnClassifierModule):
    """
    A module wrapper around the sklearn Multinomial Naive
    Bayes classifier. More information about it can be found here:
    http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html#sklearn.naive_bayes.MultinomialNB
    """
    def __init__(self):
        super().__init__()
        self.classifier = MultinomialNB()
