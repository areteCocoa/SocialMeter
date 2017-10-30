# hashtagcount.py

import re
from ..chain_links import FeatureExtractor


class HashtagCountFE(FeatureExtractor):
    def __init__(self):
        super().__init__()
        self.key = "hashtag-count"

    def extract(self, text):
        # Uses the regular expression '\W(\#[a-zA-Z]+)'
        # to get all the hashtags
        regex = r'\W(\#[a-zA-Z]+)'
        r = re.findall(regex, text)
        return len(r)
