# adjcount.py

import nltk
from ..chain_links import FeatureExtractor


class AdjectiveCounterFE(FeatureExtractor):
    def __init__(self):
        super().__init__()
        discrete_format = ["0_0", "1_2", "2<"]
        discrete_values = [0, 1, 2]
        self.set_discrete_format(discrete_format, discrete_values)
        self.key = "adjective-count"

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
