# sqlite.py

from ..chain_links import Module

import sqlite3


class SQLiteModule(Module):
    def __init__(self):
        super().__init__()
        self.connection = None

    def setup_db(self, filename):
        """
        Sets up a new database for this module with the name `filename`.

        Note that you must also call `connect_to_db` after calling
        this since it closes the connection to make sure everything
        is saved correctly.
        """
        self.connection = sqlite3.connect(filename)
        c = self.connection.cursor()
        c.execute("CREATE TABLE sentiments (input text, sentiment text)")
        self.connection.commit()
        self.connection.close()

    def connect_to_db(self, filename):
        self.connection = sqlite3.connect(filename)

    def process(self, data):
        text = data['text']
        s = data['classification']

        c = self.connection.cursor()
        c.execute("INSERT INTO sentiments VALUES (?, ?)", (text, s))

        self.connection.commit()
