# chain-links.py

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

        
class TwitterStreamModule(Module):
    def __init__(self):
        self.set_mod_type(INPUT_MOD)

    def process(self, data):
        super().process(data)
        
    def dummy_data(self):
        data = {"text" : "This is dummy data."}
        self.process(data)
        self.dummy_data()

    def start(self):
        self.dummy_data()


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
        data = "Text \"{}\" with classification \"{}\"".format(
            data["text"], data["classification"])
        super().process(data)

        
# LINKS
class Link:
    def __init__(self, owner, link_type):
        self.owner = owner
        self.link_type = link_type
        self.mods = list()

    def add_mod(self, mod):
        self.mods.append(mod)
        mod.set_handler(self.handle_mod_data)
        mod.set_id(len(self.mods))

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
    

# TEST
c = Chain()
c.add_mod(TwitterStreamModule())
c.add_mod(AdjectiveCountModule())
c.add_mod(NBClassifierModule())
c.add_mod(OutputModule())
c.set_handler(handler)
c.start_if_ready()
