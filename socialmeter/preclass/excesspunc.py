# excesspunc.py

from ..chain_links import FeatureExtractor
import nltk


class ExcessivePunctuationFE(FeatureExtractor):
    def extract(self, text):
        pos_tokens = nltk.pos_tag(nltk.word_tokenize(text))
        punc = [x for x in pos_tokens if x[1] == "."]
        punc_c = len(punc)
        d_punc_c = self.discretize_result(punc_c)
        return d_punc_c
