# pos_tag.py

import nltk
from ..chain_links import PreprocessorExtractor


class POSTagPreprocessor(PreprocessorExtractor):
    """
    Tags tokens as the POS and returns them.
    """
    def __init__(self):
        super().__init__()
        self.key = "pos-tag"

    def extract(self, text):
        if type(text) is str:
            # Tokenize first
            text = nltk.word_tokenize(text)
        return nltk.pos_tag(text)
