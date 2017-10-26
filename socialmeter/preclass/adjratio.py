# adjratio.py

from ..chain_links import FeatureExtractor

import nltk
from nltk.corpus import sentiwordnet as sw


class AdjectiveRatioFE(FeatureExtractor):
    """
    AdjectiveRatioFE counts the number of positive and
    the number of negative words in the sentence by
    using nltk to identify the adjectives and then uses
    sentiwordnet through nltk to identify a positive
    and negative score. The higher score is used to identify
    the word as either positive or negative (this is a
    dumb feature extractor). The percentage of words that
    are positive is returned.
    """
    def extract(self, text):
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        # Identify the adjectives and get a score for them,
        # and then add to the number of pos or negs
        n_pos = 0
        n_neg = 0
        for word, tag in pos_tags:
            if tag[0:2] == "JJ":
                # It is an adjective, get a score for it
                try:
                    score = sw.senti_synset("{}.a.01".format(word))
                    if score.pos_score() > score.neg_score():
                        n_pos += 1
                    else:
                        n_neg += 1
                except:
                    # found a word that isn't a word or was
                    # incorrectly identified as an adjective
                    pass
        t = n_pos + n_neg
        if t == 0:
            return 0.0
        r = n_pos / t
        return self.discretize_result(r)
