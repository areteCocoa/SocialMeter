# wordcount.py

import nltk
from ..chain_links import FeatureExtractor


class WordCountFE(FeatureExtractor):
    def extract(self, text):
        tokens = nltk.word_tokenize(text)
        return self.discretize_result(len(tokens))
