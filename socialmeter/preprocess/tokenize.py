# tokenize.py

from ..chain_links import PreprocessorExtractor
import nltk


class TokenizerPreprocessor(PreprocessorExtractor):
    """
    Tokenizes the sentence using the nltk word_tokenize
    function.
    """
    def __init__(self):
        super().__init__()
        self.key = "tokenize"

    def extract(self, text):
        t = nltk.word_tokenize(text)
        return t

