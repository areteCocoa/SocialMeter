# wordcount.py

import nltk
from ..chain_links import FeatureExtractor


class WordCountFE(FeatureExtractor):
    def __init__(self):
        super().__init__()
        self.key = "word-count"
    
    """
    WordCountFE extracts the number of tokens using nltk's pos_tag
    function.
    """
    def extract(self, text):
        tokens = nltk.word_tokenize(text)
        return self.discretize_result(len(tokens))
