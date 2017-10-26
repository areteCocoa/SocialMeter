# adjcount.py

import nltk
from ..chain_links import FeatureExtractor


class AdjectiveCounterFE(FeatureExtractor):
    """
    The AdjectiveCounterFE class counts the number of adjectives
    using the nltk pos_tag function and returns the discrete result.
    """
    def extract(self, text):
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        adj_count = 0
        for word, tag in pos_tags:
            if tag[0:2] == "JJ":
                adj_count += 1
        return self.discretize_result(adj_count)
