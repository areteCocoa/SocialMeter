# twitterstream.py

from ..chain_links import InputModule

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import pandas as pd

import json


class TwitterStreamModule(InputModule, StreamListener):
    """
    The TwitterStreamModule uses the TwitterStream API to fetch
    data. It must be configured with the API data using a json config
    file.
    """
    def __init__(self):
        self.allow_empty = False

    def load_config(self, filename):
        """
        Loads the json config file with name `filename` and parses it
        to the required fields.
        """
        config = json.load(open(filename, 'r'))["twitter"]
        self.set_access_token(config["access_token"])
        self.set_access_token_secret(config["access_token_secret"])
        self.set_consumer_key(config["consumer_key"])
        self.set_consumer_secret(config["consumer_secret"])

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
        self.handler(parsed)

    # StreamListener
    def on_data(self, data):
        self.parse_response(data)
        return True

    def on_error(self, status_code):
        print("There was a status error! {}".format(status_code))
