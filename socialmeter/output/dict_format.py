# output.dict_format.py

from ..chain_links import Module, OUTPUT_MOD


class OutputModule(Module):
    def __init__(self):
        self.set_mod_type(OUTPUT_MOD)

    def process(self, data):
        # Convert dataframe to dict
        d = data.to_dict()

        # If we don't have text
        if "text" not in d.keys():
            d["text"] = "(text not found)"

        super().process(d)
