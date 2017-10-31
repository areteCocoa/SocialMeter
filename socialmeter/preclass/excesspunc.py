# excesspunc.py

from ..chain_links import FeatureExtractor
import nltk


class ExcessivePunctuationFE(FeatureExtractor):
    def __init__(self):
        super().__init__()
        self.key = "excessive-punctuation"
    
    """
    The ExcessivePunctuationFE class counts the number of
    punctuations greater than 1 using the nltk pos_tag function.

    The pos_tag function ensures that '...' and '..' are tagged
    as 1 and 2 characters respectively.
    """
    def extract(self, text):
        pos_tokens = nltk.pos_tag(nltk.word_tokenize(text))
        conseq_count = 0
        total_count = 0
        for (token, pos) in pos_tokens:
            if pos == ".":
                conseq_count += 1
            elif pos == ":" and token == "...":
                conseq_count += 3
            else:
                if conseq_count > 1:
                    total_count += 1
                conseq_count = 0

        if conseq_count > 1:
            total_count += 1
                
        d_punc_c = self.discretize_result(total_count)
        return d_punc_c
