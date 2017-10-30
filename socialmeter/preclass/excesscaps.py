# excesscaps.py

import nltk
from ..chain_links import FeatureExtractor


class ExcessiveCapitalsFE(FeatureExtractor):
    def __init__(self):
        super().__init__()
        self.key = "excessive-caps"
    
    """
    The ExcessiveCapitalsFE class counts the number of words with
    all capitals in the sentence and then returns it.
    """
    def extract(self, text):
        all_caps = 0
        tokens = text.split(' ')
        for t in tokens:
            if t.upper() == t:
                all_caps += 1
        t = len(tokens)
        if t == 0:
            return 0
        perc = all_caps / t
        return self.discretize_result(perc)
