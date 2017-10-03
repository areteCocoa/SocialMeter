# excesspunc.py

from ..chain_links import FeatureExtractor
import nltk


class ExcessivePunctuationFE(FeatureExtractor):
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
