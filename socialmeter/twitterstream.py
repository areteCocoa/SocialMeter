# twitterstream.py

from socialmeter.chain_links import Module, INPUT_MOD

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import pandas as pd

import json


class TwitterStreamModule(Module, StreamListener):
    # Object
    def __init__(self):
        self.set_mod_type(INPUT_MOD)
        self.allow_empty = False

    # Load the config file and set the access and consumer keys
    def load_config(self, filename):
        config = json.load(open(filename, 'r'))["twitter"]
        self.set_access_token(config["access_token"])
        self.set_access_token_secret(config["access_token_secret"])
        self.set_consumer_key(config["consumer_key"])
        self.set_consumer_secret(config["consumer_secret"])

    # Module
    def process(self, data):
        super().process(data)

    def set_term(self, term):
        self.term = term

    def set_access_token(self, token):
        self.access_token = token

    def set_access_token_secret(self, secret):
        self.access_token_secret = secret

    def set_consumer_key(self, key):
        self.consumer_key = key

    def set_consumer_secret(self, secret):
        self.consumer_secret = secret

    def start(self):
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.stream = Stream(auth, self)
        self.stream.filter(track=self.term)

    def parse_response(self, response):
        parsed = json.loads(response)
        if self.column_format() is None:
            print("Warning: did not find a column format for\
 TwitterStreamModule, using all the keys from the Twitter objects")
            self.set_column_format(parsed.keys())
        series_data = dict()
        for k in self.column_format():
            if k in parsed.keys():
                series_data[k] = parsed[k]
            elif self.allow_empty is False and k == "text":
                return
        df = pd.Series(series_data)

        self.handler(self, df)

    # StreamListener
    def on_data(self, data):
        self.parse_response(data)
        return True

    def on_error(self, status_code):
        print("There was a status error! {}".format(status_code))
