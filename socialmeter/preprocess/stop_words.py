# stop_words.py

import nltk
from ..chain_links import PreprocessorExtractor


class StopWordsPreprocessor(PreprocessorExtractor):
    """
    Uses an input list of stop words and filters them from
    the input.

    This can be useful for removing potentially useless words
    from the input datas, such as "the" and "a" (although they
    may also be useful.

    Note that the user must set the set of stop words using
    set_stop_words and add_stop_word(s) using their own dataset.
    Although the README should direct you to some appropriate
    datasets, I don't feel comfortable including them in the
    project.
    """
    def __init__(self):
        super().__init__()
        self.key = "stop-words"
        self.stop_words = list()

    def set_stop_words(self, words):
        self.stop_words = words

    def add_stop_word(self, word):
        self.stop_words.append(word)

    def add_stop_words(self, words):
        for w in words:
            self.stop_words.append(w)

    def extract(self, text):
        t = text.split(' ')
        l = list()
        for t in t:
            if t not in self.stop_words:
                l.append(t)
        s = ' '.join(l)
        return s
