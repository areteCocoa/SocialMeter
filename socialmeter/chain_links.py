# chain-links.py

import pandas as pd

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json


INPUT_MOD = "input-module"
PRECLASS_MOD = "preclass-module"
CLASS_MOD = "class-module"
OUTPUT_MOD = "output-module"

INPUT_LINK = "input-link"
PRECLASS_LINK = "pre-classification-link"
CLASS_LINK = "classification-link"
OUTPUT_LINK = "output-link"


# MODULES
class Module:
    def set_mod_type(self, mod_type):
        self.mod_type = mod_type

    def process(self, data):
        self.handler(self, data)

    def set_handler(self, handler):
        self.handler = handler

    def set_id(self, new_id):
        self.identifier = new_id

    def set_column_format(self, c_format):
        self.__column_format = c_format[:]

    def column_format(self):
        return self.__column_format

        
class TwitterStreamModule(Module, StreamListener):
    # Object
    def __init__(self):
        self.set_mod_type(INPUT_MOD)

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
        df = pd.Series(series_data)
        
        self.handler(self, df)

    # StreamListener
    def on_data(self, data):
        self.parse_response(data)
        return True

    def on_error(self, status_code):
        print("There was a status error! {}".format(status_code))


class AdjectiveCountModule(Module):
    def __init__(self):
        self.set_mod_type(PRECLASS_MOD)

    def process(self, data):
        data["features"]["adj-count"] = 2
        super().process(data)


class NBClassifierModule(Module):
    def __init__(self):
        self.set_mod_type(CLASS_MOD)

    def process(self, data):
        data["classification"] = "positive"
        super().process(data)

        
class OutputModule(Module):
    def __init__(self):
        self.set_mod_type(OUTPUT_MOD)

    def process(self, data):
        text = None
        if "text" in data.keys():
            text = data["text"]
        else:
            text = "(text not found)"
        data = "Text \"{}\" with classification \"{}\"".format(
            text, data["classification"])
        super().process(data)

        
# LINKS
class Link:
    def __init__(self, owner, link_type):
        self.owner = owner
        self.link_type = link_type
        self.mods = list()
        self.column_format = None

    def add_mod(self, mod):
        self.mods.append(mod)
        mod.set_handler(self.handle_mod_data)
        mod.set_id(len(self.mods))
        if self.column_format is not None:
            mod.set_column_format(self.column_format)

    def process(self, data):
        self.mods[0].process(data)
        
    def handle_mod_data(self, sender, data):
        if sender.identifier == len(self.mods):
            # Finished all the modules in the link, time to pass up to
            # the chain
            self.handler(self, data)
        else:
            self.mods[sender.identifier].process(data)

    def set_handler(self, handler):
        self.handler = handler

    def set_column_format(self, c_format):
        self.column_format = c_format[:]
        for m in self.mods:
            m.set_column_format(self.column_format)

    def is_empty(self):
        return len(self.mods) == 0
        

# CHAINS
class Chain:
    def __init__(self):
        self.input_link = Link(self, INPUT_LINK)
        self.input_link.set_handler(self.link_finished)
        
        self.preclass_link = Link(self, PRECLASS_LINK)
        self.preclass_link.set_handler(self.link_finished)
        
        self.class_link = Link(self, CLASS_LINK)
        self.class_link.set_handler(self.link_finished)
        
        self.output_link = Link(self, OUTPUT_LINK)
        self.output_link.set_handler(self.link_finished)

    def set_handler(self, handler):
        self.handler = handler

    def set_column_format(self, c_format):
        self.column_format = c_format
        
        self.input_link.set_column_format(c_format)
        self.preclass_link.set_column_format(c_format)
        self.class_link.set_column_format(c_format)
        self.output_link.set_column_format(c_format)
        
    def add_mod(self, mod):
        mod_type = mod.mod_type
        if mod_type == INPUT_MOD:
            self.input_link.add_mod(mod)
        elif mod_type == PRECLASS_MOD:
            self.preclass_link.add_mod(mod)
        elif mod_type == CLASS_MOD:
            self.class_link.add_mod(mod)
        elif mod_type == OUTPUT_MOD:
            self.output_link.add_mod(mod)

    def start_if_ready(self):
        if not self.input_link.is_empty()\
           and not self.preclass_link.is_empty()\
           and not self.class_link.is_empty()\
           and not self.output_link.is_empty():
            self.input_link.mods[0].start()
        else:
            if self.input_link.is_empty():
                print("Not ready to start, input link is empty.")
            if self.preclass_link.is_empty():
                print("Not ready to start, preclass link is empty.")
            if self.class_link.is_empty():
                print("Not ready to start, class link is empty.")
            if self.output_link.is_empty():
                print("Not ready to start, output link is empty.")

    def link_finished(self, sender, data):
        if sender.link_type == INPUT_LINK:
            data["features"] = dict()
            self.preclass_link.process(data)
        elif sender.link_type == PRECLASS_LINK:
            self.class_link.process(data)
        elif sender.link_type == CLASS_LINK:
            self.output_link.process(data)
        else:
            self.handler(data)


def handler(data):
    print(data)
    

## TEST

c = Chain()
c.column_format = ["username", "text", "classification", "features"]

# Load JSON configuration add use it to configure the TSModule
config = json.load(open("../config.json", 'r'))["twitter"]
ts = TwitterStreamModule()
ts.set_access_token(config["access_token"])
ts.set_access_token_secret(config["access_token_secret"])
ts.set_consumer_key(config["consumer_key"])
ts.set_consumer_secret(config["consumer_secret"])
ts.set_column_format([])
ts.set_term("thomasjring")


c.add_mod(ts)
c.add_mod(AdjectiveCountModule())
c.add_mod(NBClassifierModule())
c.add_mod(OutputModule())
c.set_handler(handler)
c.start_if_ready()
