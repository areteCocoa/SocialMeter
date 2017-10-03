# excesscaps.py

import nltk
from ..chain_links import FeatureExtractor


class ExcessiveCapitalsFE(FeatureExtractor):
    def extract(self, text):
        all_caps = 0
        tokens = nltk.word_tokenize(text)
        for t in tokens:
            if t.upper() == t:
                all_caps += 1
        t = len(tokens)
        if t == 0:
            return 0
        perc = all_caps / t
        return self.discretize_result(perc)