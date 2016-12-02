"""
This file is part of the fermi-bot project.
"""

import collections


class Message:
    def __init__(self):
        self.text = None
        self.user = None

User = collections.namedtuple("User", ['ip', 'id'])
