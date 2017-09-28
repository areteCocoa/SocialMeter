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

    def set_column_format(self, c_format):
        self.__column_format = c_format[:]

    def column_format(self):
        return self.__column_format


class FeatureExtractorModule(Module):
    def __init__(self, extractor_class):
        self.set_mod_type(PRECLASS_MOD)
        self.feature_extractor = extractor_class
        self.key = "{}".format(extractor_class)

    def set_key(self, key):
        self.key = key

    def process(self, data):
        if "text" in data.keys():
            text = data["text"]
            data[self.key] = self.feature_extractor.extract(text)
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

            # We have to add a column for the new feature
            new_columns = self.column_format + [mod.key]
            self.set_column_format(new_columns)
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
