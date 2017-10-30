# hashtag.py

import re
from ..chain_links import PreprocessorExtractor


class HashtagPreprocessor(PreprocessorExtractor):
    """
    Reads through the text and replaces all instances
    of hashtags, #funny, #notfunny, with HT_FUNNY and
    HT_NOTFUNNY.

    This is useful because it eliminates the variance of
    case in analyzing these hashtags, and two, allows the
    hashtag tokens to be more easily identified later in
    the chain. This is also useful because nltk will not
    tokenize hashtags as a single token, but this
    'hashtag symbol' (HT_HASHTAGTEXT) will be.
    """
    def __init__(self):
        super().__init__()
        self.key = "hashtag-pre"

    def extract(self, text):
        regex = r'\W(\#[a-zA-Z]+)'
        new = re.sub(regex, self.repl, text)
        return new

    def repl(self, match):
        m = match.group(0).split("#")[1]
        s = " HT_{}".format(m.upper())
        return s
