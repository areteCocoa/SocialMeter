# ngram.py

from ..chain_links import PreprocessorExtractor


class NGramPreprocessor(PreprocessorExtractor):
    def __init__(self):
        super().__init__()
        self.key = "ngram-pre"

    # http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
    def extract(self, text):
        input_list = text.split(' ')
        return zip(*[input_list[i:] for i in range(1)])

