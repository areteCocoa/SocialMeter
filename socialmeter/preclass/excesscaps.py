# excesscaps.py

from ..chain_links import FeatureExtractor


class ExcessiveCapitalsFE(FeatureExtractor):
    def extract(self, text):
        caps = 0
        for ch in text:
            if ch.lower() != ch:
                caps += 1
        return self.discretize_result(caps)
