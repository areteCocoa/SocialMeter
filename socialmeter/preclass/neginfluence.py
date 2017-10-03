# neginfluence.py

import nltk
from ..chain_links import FeatureExtractor


class NegativeInfluenceFE(FeatureExtractor):
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