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

    column_format : List(String)
    A list of strings of fields used in the DataFrame. This is also set by
    the Link object and should not be changed manually.
    """
    def set_mod_type(self, mod_type):
        self.mod_type = mod_type

    def process(self, data):
        return data

    def set_column_format(self, c_format):
        self.__column_format = c_format[:]

    def column_format(self):
        return self.__column_format


class InputModule(Module):
    """
    The InputModule is any module that feeds new data that is not classified
    into the system. It is unique from a Module because it has possible
    additional threading possibilities.

    For example:
    Scenario 1 - Text file
    Classifying text from a file is straightforward, and data is passed
    in after being read to the SMeter object.

    Scenario 2 - API Calls
    Listening on a port to the TwitterStreamAPI requires that all handling
    be done on a different thread. Therefore, all text handling needs to
    be called through a handler

    Scenario 3 - API Calls on a new thread
    If the TwitterStreamAPI is using a significant amount of power and
    needs to use all of that power on the thread handling and preparing
    the data, it may be adventageous to spawn a new thread (possibly
    from a pool of threads) for the data to be processed on so the API
    thread can continue without being blocked.
    """
    def process(self, data):
        return data

    def set_handler(self, handler):
        self.handler = handler


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
        return super().process(data)


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
        try:
            self.key = self.feature_extractor.key
        except:
            self.key = "{}".format(extractor_class)

    def __str__(self):
        s = "FeatureExtractorModule<{}> {}\n"\
            .format(self.feature_extractor, hex(id(self)))
        return s

    def with_fe_class(fe_class):
        return FeatureExtractorModule(fe_class())

    def set_key(self, key):
        self.key = key

    def process(self, data):
        if "text" in data.keys():
            text = data["text"]
            data[self.key] = self.feature_extractor.extract(text)
        return super().process(data)


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
        if self.column_format is not None:
            mod.set_column_format(self.column_format)

    def process(self, data):
        # For each module in this chain, process it
        for m in self.mods:
            data = m.process(data)
        return data

    def set_column_format(self, c_format):
        self.column_format = c_format[:]
        for m in self.mods:
            m.set_column_format(self.column_format)

    def is_empty(self):
        return len(self.mods) == 0


class PreprocessorLink(Link):
    def __init__(self, owner):
        super().__init__(owner, PREPROCESS_LINK)

    def process(self, data):
        return super().process(data)
        # TODO: Option for preprocessors to set the text to
        # the changed text


class SMeter:
    """
    The SMeter class is responsible for managing all types of modules, as
    well as the passing of data between them.

    SMeter is the replacement class for what was previously the Chain
    class. It is different in that it has a different structure than
    the Chain class, specifically in how the individual modules are
    handled vs the links of modules. This was changed because it allows
    for more specific handling with the checking code.
    """
    def __init__(self):
        self.input_mod = None
        self.preprocess_link = PreprocessorLink(self)
        self.preclass_link = Link(self, PRECLASS_LINK)
        self.class_mod = None
        self.output_mod = None

        self.column_format = None
        self.handler = None

    def start_if_ready(self):
        # TODO: Change this into checking if they're empty one by
        # one and printing which are not set, and then the else case
        # is starting the input module.
        if self.input_mod is not None\
           and not self.preprocess_link.is_empty()\
           and not self.preclass_link.is_empty()\
           and self.class_mod is not None\
           and self.output_mod is not None:
            self.input_mod.start()
        else:
            print("Not ready to start.")

    #  Module finished handlers
    def new_input(self, input_data):
        """
        Called when there is new input from the input module.
        """
        data = self.preprocess_link.process(input_data)
        self.preprocess_finished(data)

    def preprocess_finished(self, data):
        """
        Called when the preprocessing modules have all finished.
        """
        data = self.preclass_link.process(data)
        self.preclass_finished(data)

    def preclass_finished(self, data):
        """
        Called when the preclass modules have all finished.
        """
        data = self.class_mod.process(data)
        self.finished_classify(data)

    def finished_classify(self, data):
        """
        Called when the classifier is done classifying the data.
        """
        data = self.output_mod.process(data)
        self.output_finished(data)

    def output_finished(self, data):
        """
        Called when the output module is done.
        """
        self.handler(data)

    #  Overriding `Object` methods (excluding __init__)

    def __str__(self):
        s = "SMeter {}:\n".format(hex(id(self)))
        s += "\tcolumn_format: {}\n".format(self.column_format)
        # TODO: Print the input mod, the preprocess link, etc.
        return s

    #  Getters, setters and adders

    def set_handler(self, handler):
        self.handler = handler

    def set_column_format(self, c_format):
        self.column_format = c_format

        if self.input_mod is not None:
            self.input_mod.set_column_format(c_format)
        self.preprocess_link.set_column_format(c_format)
        self.preclass_link.set_column_format(c_format)
        if self.class_mod is not None:
            self.class_mod.set_column_format(c_format)
        if self.output_mod is not None:
            self.output_mod.set_column_format(c_format)

    def add_column(self, column_n):
        new_columns = self.column_format + [column_n]
        self.set_column_format(new_columns)

    def set_input_mod(self, input_mod):
        self.input_mod = input_mod
        self.input_mod.set_column_format(self.column_format)
        self.input_mod.set_handler(self.new_input)

    def add_preprocess_mod(self, pp_mod):
        self.preprocess_link.add_mod(pp_mod)
        pp_mod.set_column_format(self.column_format)
        self.add_column(pp_mod.key)

    def add_preclass_mod(self, pc_mod):
        self.preclass_link.add_mod(pc_mod)
        pc_mod.set_column_format(self.column_format)
        self.add_column(pc_mod.key)

    def set_class_mod(self, c_mod):
        self.class_mod = c_mod
        self.class_mod.set_column_format(self.column_format)

    def set_output_mod(self, o_mod):
        self.output_mod = o_mod
        self.output_mod.set_column_format(self.column_format)
