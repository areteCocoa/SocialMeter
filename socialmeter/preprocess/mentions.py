# mentions.py

import re
from ..chain_links import PreprocessorExtractor


class MentionPreprocessor(PreprocessorExtractor):
    """
    Reads through the text and replaces all instances
    of mentions, @thomasjring, with MN_THOMASJRING

    This is useful because (1) it eliminates the variance of
    case in analyzing these mentions, (2) it allows the
    mention tokens to be more easily identified later in
    the chain, and (3) nltk will not tokenize mentions as a 
    single token, but this 'mention symbol' (MN_USERNAME) 
    will be.
    """
    def __init__(self):
        super().__init__()
        self.key = "mention-pre"
        
    def extract(self, text):
        regex = r'\W(\@[a-zA-Z]+)'
        new = re.sub(regex, self.repl, text)
        return new

    def repl(self, match):
        m = match.group(0).split("#")[1]
        s = " MN_{}".format(m.upper())
        return s
