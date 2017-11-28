# facebookgraph.py

# http://nodotcom.org/python-facebook-tutorial.html

from ..chain_links import InputModule

import json

import facebook as fb


class FacebookGraphModule(InputModule):
    """
    This module is a Proof-of-concept that both (1) Facebook can
    be integrated within this framework and (2) that this framework
    can be extended and usable with a small amount of code.

    Your config file should include a 'facebook' dict with an
    access_token field (see the link at the top of the file on details
    on how to create this.

    If one wishes to implement a fully functional FacebookGraph module,
    they will likely need to look into a more fully functional facebook
    library for Python, as the one included in this one (the most
    updated facebook library for python) does not include many of the
    features such as pagnation that are required to do large scale
    requests.
    """
    def __init__(self):
        self.graph = None
        self.sources = list()

    def load_config(self, filename):
        config = json.load(open(filename, 'r'))["facebook"]
        token = config['access_token']
        self.graph = fb.GraphAPI(access_token=token)

    def add_source(self, source):
        self.sources.append(source)

    def start(self):
        if self.graph is None:
            print("Attempted to start FacebookGraphModule before it was \
configured!")
        me = self.graph.get_object('/me')
        my_id = me['id']
        response = self.graph.get_object("/{}/posts".format(my_id))
        posts = response['data']

        for p in posts:
            if 'text' not in p.keys():
                if 'message' in p.keys():
                    p['text'] = p['message']
                elif 'story' in p.keys():
                    p['text'] = p['story']
            self.handler(p)


# posts = response['data']

# for post in posts:
#     text = None
#     if 'message' in post.keys():
#         text = post['message']
#     elif 'story' in post.keys():
#         text = post['story']
#     print("{}: {}".format(post['created_time'], text))
