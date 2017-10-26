# excesspunc.py

from ..chain_links import FeatureExtractor
import nltk


class ExcessivePunctuationFE(FeatureExtractor):
    """
    The ExcessivePunctuationFE class counts the number of
    punctuations greater than 1 using the nltk pos_tag function.

    The pos_tag function ensures that '...' and '..' are tagged
    as 1 and 2 characters respectively.
    """
    def extract(self, text):
        pos_tokens = nltk.pos_tag(nltk.word_tokenize(text))
        ex_punc_word = 0
        ex_punc_sent = 0
        for (token, pos) in pos_tokens:
            if pos == ".":
                ex_punc_word += 1
            else:
                if ex_punc_word > 1:
                    ex_punc_sent += 1
                ex_punc_word = 0

        d_punc_c = self.discretize_result(ex_punc_sent)
        return d_punc_c
