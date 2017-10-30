# emoticon.py

from ..chain_links import FeatureExtractor


class EmoticonSentimentFE(FeatureExtractor):
    def __init__(self):
        super().__init__()
        self.key = "emoticon-sentiment"

    def set_file(self, f):
        """
        Initializes the opened file `f` and parses
        through the data. This should be called before
        any extracting is done.
        """
        self.sentiments = dict()
        l = f.readline()
        while l is not '':
            s = l.strip().split('\t')
            emo = s[0]
            sent = int(s[1].strip())
            self.sentiments[emo] = sent
            l = f.readline()

    def extract(self, text):
        if text in self.sentiments.keys():
            return self.sentiments[text]
        else:
            return 0
