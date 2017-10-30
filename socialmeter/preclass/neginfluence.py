# neginfluence.py

import nltk
from ..chain_links import FeatureExtractor


class NegativeInfluenceFE(FeatureExtractor):
    def __init__(self):
        super().__init__()
        self.key = "negative-influence"
    
    """
    NegativeInfluenceFE extracts the number of 'not' tokens in the
    sentence and discretizes the result to odd or even number.
    """
    def extract(self, text):
        tokens = nltk.word_tokenize(text)
        has_not = False
        for word in tokens:
            if word.lower() == "not" or word.lower() == "n't":
                has_not = not has_not
        r = None
        if has_not is False:
            r = 0
        else:
            r = 1
        r = self.discretize_result(r)
        return r
