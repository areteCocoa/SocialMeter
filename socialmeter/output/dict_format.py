# output.dict_format.py

from ..chain_links import Module


class OutputModule(Module):
    """
    OutputModule takes the pandas DataFrame and converts it
    to a dict.

    It ensures that there is a text field in the dictionary.
    """
    def process(self, data):
        # Convert dataframe to dict
        d = data.to_dict()

        # If we don't have text
        if "text" not in d.keys():
            d["text"] = "(text not found)"

        return super().process(d)
