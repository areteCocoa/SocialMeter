# adjcount.py

import nltk


class AdjectiveCounterFE():
    def extract(text):
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        adj_count = 0
        for word, tag in pos_tags:
            if tag[0:2] == "JJ":
                adj_count += 1
        return adj_count
