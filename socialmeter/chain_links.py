# chain-links.py

# This group of varialbes are used to define the type of module.
#
# The chain class uses these to place modules in the correct
# link, and changes how they're utilized.
INPUT_MOD = "input-module"
PREPROCESS_MOD = "preprocess-module"
PRECLASS_MOD = "preclass-module"
CLASS_MOD = "class-module"
OUTPUT_MOD = "output-module"

# This group of variables are used to define the type of link.
INPUT_LINK = "input-link"
PREPROCESS_LINK = "preprocess-link"
PRECLASS_LINK = "pre-classification-link"
CLASS_LINK = "classification-link"
OUTPUT_LINK = "output-link"


class Module:
    """
    The Module class represents a single action in the chain and
    defines how to do it.

    There are several members of Module that are used by the
    owning Chain and Link objects, and several of them should
    only be set by Chain and Link objects.

    Members
    -------
    mod_type : String
    The type of the module. Should be a value from one of the constants
    above.

    handler : function
    A handler function that is called when the module is finished processing
    the data. In most cases, this will be set by the Chain and Link objects
    themselves.

    identifier : int
    An identifier number that is set by the owning Link object and used
    to identify modules in the Link.

    column_format : List(String)
    A list of strings of fields used in the DataFrame. This is also set by
    the Link object and should not be changed manually.
    """
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

    def deep_copy(self):
        c = type(self)()
        c.mod_type = self.mod_type
        c.handler = self.handler
        c.identifier = self.identifier
        return c


class PreprocessorExtractorModule(Module):
    """PreprocessorExtractorModule is a wrapper class that performs
    general preprocessing operations using the PreprocessorExtractor
    class and it's subclasses.
    """
    def __init__(self, preprocessor):
        self.set_mod_type(PREPROCESS_MOD)
        self.preprocess_extractor = preprocessor
        self.key = "{}".format(preprocessor)

    def set_key(self, key):
        self.key = key

    def process(self, data):
        if "text" in data.keys():
            text = data["text"]
            data[self.key] = self.preprocess_extractor.extract(text)
        super().process(data)

    def deep_copy(self):
        c = type(self)(self.feature_extractor)
        c.mod_type = self.mod_type
        c.handler = self.handler
        c.identifier = self.identifier
        return c


class PreprocessorExtractor():
    def extract(self, text):
        return None


class FeatureExtractorModule(Module):
    """
    The FeatureExtractorModule class is a wrapper class that performs
    general operations using the FeatureExtractor class.

    If you want to create a new Feature for your classifier, you
    will want to create a subclass of FeatureExtractor, not
    FeatureExtractorModule.

    Members
    -------
    feature_extractor : Object that subclasses FeatureExtractor
    This object is used to extract the feature from the text in the
    process function.

    key : String
    The key in column_format that corresponds to this feature. This
    is used to set the correct property in the DataFrame.
    """
    def __init__(self, extractor_class):
        self.set_mod_type(PRECLASS_MOD)
        self.feature_extractor = extractor_class
        self.key = "{}".format(extractor_class)

    def __str__(self):
        s = "FeatureExtractorModule<{}> {}\n"\
            .format(self.feature_extractor, hex(id(self)))
        return s

    def set_key(self, key):
        self.key = key

    def process(self, data):
        if "text" in data.keys():
            text = data["text"]
            data[self.key] = self.feature_extractor.extract(text)
        super().process(data)

    def deep_copy(self):
        c = type(self)(self.feature_extractor)
        c.mod_type = self.mod_type
        c.handler = self.handler
        c.identifier = self.identifier
        return c


class FeatureExtractor():
    """
    FeatureExtractor is class responsible for extracting a specific
    feature from a text. It is also responsible for discretizing the
    data.

    Discrete ranges and formats should be set with .set_discrete_format().
    It should be set to a list of strings that represent ranges.

    Discrete Formatting
    -------------------
    For a range of values, specify using inclusive and exclusive
    formatted discrete values.
    Exclusive:
    "0.0-0.2"

    Inclusive:
    "0.0_0.2"

    For values that extend after or before a certain value, use
    greater than or less than. Note that the value should always
    preceed the operator in these formats.
    Greater Than:
    2.0<

    Less Than:
    5.0>

    Members
    -------
    discrete_format : List(String)
    The discrete formatting strings. Read above on usage.

    discrete_values : List
    The list of values to set corresponding to each format.
    """
    def __init__(self):
        self.discrete_format = None
        self.discrete_values = None

    def set_discrete_format(self, discrete_f, discrete_v):
        self.discrete_format = discrete_f
        self.discrete_values = discrete_v

    def extract(self, text):
        return None

    def discretize_result(self, result):
        if self.discrete_format is None:
            return result
        else:
            for f in self.discrete_format:
                cmp_r = self._compare_discrete_f(f, result)
                if cmp_r is not None:
                    return self.discrete_values[
                        self.discrete_format.index(cmp_r)]
        return None

    def _compare_discrete_f(self, d_f, cmp_v):
        """
        Compares a discrete format and a value, returns a discrete
        format if it fits within that format, None otherwise.
        """
        (t, v) = self._parse_d_format(d_f)
        if t == "i" or t == "e":
            # There are two values to compare
            v0 = v[0]
            v1 = v[1]
            if t == "e":
                if v0 < cmp_v and cmp_v < v1:
                    return d_f
                else:
                    return None
            else:
                if v0 <= cmp_v and cmp_v <= v1:
                    return d_f
                else:
                    return None
        elif t == "gt" or t == "lt":
            # There is one value to compare
            if t == "gt":
                if v < cmp_v:
                    return d_f
                else:
                    return None
            else:
                if v > cmp_v:
                    return d_f
                else:
                    return None
        # There was an error and we return none
        return None

    def _parse_d_format(self, d_format):
        """
        An internal method used to parse a discrete format
        string. Returns (format_type, (value1, [value2])),
        where format_type is a string signifying if it is
        an inclusive ("i"), exclusive ("e"), greater than ("gt")
        or less than ("lt") discrete format. If no valid format
        is found, None is returned.
        """
        excl = d_format.split("-")
        if len(excl) != 1:
            n1 = float(excl[0])
            n2 = float(excl[1])
            return ("e", (n1, n2))

        incl = d_format.split("_")
        if len(incl) != 1:
            n1 = float(incl[0])
            n2 = float(incl[1])
            return ("i", (n1, n2))

        gt = d_format.split("<")
        if len(gt) != 1:
            n = float(gt[0])
            return ("gt", (n))

        lt = d_format.split(">")
        if len(lt) != 1:
            n = float(lt[0])
            return ("lt", (n))

        # We couldn't find a symbol of a correct discrete
        # format, so we return None.
        return None


class Link:
    """
    The Link class binds modules of a single type together. It is
    responsible for managing the modules and that the data is passed
    in the correct order.
    """
    def __init__(self, owner, link_type):
        self.owner = owner
        self.link_type = link_type
        self.mods = list()
        self.column_format = None

    def __str__(self):
        s = "{} {}\n".format(self.link_type, hex(id(self)))
        for m in self.mods:
            s = "{}\t{}".format(s, m)
        return s
        
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

    def deep_copy(self, new_owner):
        """
        Returns a new copy of this link and all of the modules
        """
        c = Link(new_owner, self.link_type)
        mods = list()
        for m in self.mods:
            mods.append(m.deep_copy())
        c.mods = mods
        return c


class Chain:
    """
    The Chain class is responsible for managing all links and modules.
    It is also responsible for data being handled correctly.
    """
    def __init__(self):
        self.input_link = Link(self, INPUT_LINK)
        self.input_link.set_handler(self.link_finished)

        self.preprocess_link = Link(self, PREPROCESS_LINK)
        self.preprocess_link.set_handler(self.link_finished)
        
        self.preclass_link = Link(self, PRECLASS_LINK)
        self.preclass_link.set_handler(self.link_finished)

        self.class_link = Link(self, CLASS_LINK)
        self.class_link.set_handler(self.link_finished)

        self.output_link = Link(self, OUTPUT_LINK)
        self.output_link.set_handler(self.link_finished)

        self.column_format = None

    def __str__(self):
        s = "Chain {}:\n".format(hex(id(self)))
        s = "{}\tcolumn_format: {}\n".format(s, self.column_format)
        for l in [self.input_link, self.preprocess_link,
                  self.preclass_link, self.class_link,
                  self.output_link]:
            s = "{}\t{}".format(s, l)
        return s

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

    def deep_copy(self):
        """
        Returns a copy of the chain and every link and module.
        """
        c = Chain()
        c.column_format = self.column_format
        c.input_link = self.input_link.deep_copy(c)
        c.preclass_link = self.preclass_link.deep_copy(c)
        c.class_link = self.class_link.deep_copy(c)
        c.output_link = self.output_link.deep_copy(c)
        return c

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
            self.preprocess_link.process(data)
        elif sender.link_type == PREPROCESS_LINK:
            self.preclass_link.process(data)
        elif sender.link_type == PRECLASS_LINK:
            self.class_link.process(data)
        elif sender.link_type == CLASS_LINK:
            self.output_link.process(data)
        else:
            self.handler(data)
