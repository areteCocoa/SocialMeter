# textcloud.py

from ..chain_links import Module

import os
import sys
import time
import random


class TextCloudModule(Module):
    """
    TextCloudModule takes the input of the new data and prints
    it to the console in a "cloud" format. This consists of a few
    steps:
    1. The terminal/console is cleared of any and all text
    2. This module determines the size of the screen
    3. As text enters, it is placed into the queue
    4. Every ~5 seconds there is a text placed at a random row
    in the terminal

    The effect should be a wallpaper-esque look that is updated
    with live, analyzed data. This also gives the user an opportunity
    to look over their classifications.
    """
    def __init__(self):
        super().__init__()
        self.last_displayed = time.time()
        self.queue = list()
        self.delay = 3
        self.displayed_rows = list()

    def process(self, data):
        if len(self.queue) >= 100:
            # Remove a random item so we don't overflow the memory
            index = int((random.random() * 100) % 100)
            self.queue.pop(index)

        # Build the string to be displayed
        formatted = "[{}] {}".format(data['classification'],
                                     data['text'])
        self.queue.append(formatted)

        # If it's time to add a new string to the console, do it
        if len(self.displayed_rows) == 0:
            TextCloudModule.clear_console()
        self.add_string_if_appropriate()
        return None

    def add_string_if_appropriate(self):
        t = time.time()
        if t - self.last_displayed >= self.delay:
            self.display_string()
            self.last_displayed = time.time()

    def display_string(self):
        s = self.queue.pop(0)
        # Select a random row
        r = int(random.random() * TextCloudModule.console_dimensions()[0])
        TextCloudModule.clear_row(r)
        TextCloudModule.print_at_location(0, r, s)
        self.displayed_rows.append(r)

    def console_dimensions():
        """
        Uses the 'stty size' command from the os to read the size
        of the console and then convert it to a row and column int
        objects.
        """
        row, column = os.popen('stty size', 'r').read().split()
        return (int(row), int(column))

    def clear_console():
        """
        Uses regular printing to print a newline from the top to
        bottom of the console, clearing the console.
        """
        for x in range(TextCloudModule.console_dimensions()[0]):
            print()

    def clear_row(row):
        """
        Clears a single row by print a row of space characters.
        """
        width = TextCloudModule.getConsoleDimensions()[1]
        whiteString = " " * width
        TextCloudModule.print_at_location(row, 0, whiteString)

    def print_at_location(row, column, text):
        """
        Prints the string text at the specified location (x, y).
        """
        dimension = TextCloudModule.console_dimensions()
        if dimension[0] < column or dimension[1] < row:
            print(dimension[0], dimension[1])
        else:
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (column, row, text))
            sys.stdout.flush()
