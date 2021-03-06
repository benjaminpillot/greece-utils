# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

# __all__ = []
# __version__ = '0.1'
__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2018, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'

# import

immutable_types = {int, str}


class Frozen(object):
    def __init__(self, value):
        self._value = value

    def __getattribute__(self, name):
        if name == '_value':
            return super(Frozen, self).__getattribute__(name)
        v = getattr(self._value, name)
        return v if v.__class__ in immutable_types else freeze(v)

    def __setattr__(self, name, value):
        if name == '_value':
            super(Frozen, self).__setattr__(name, value)
        else:
            raise Exception("Can't modify frozen object {0}".format(self._value))


def freeze(value):
    return Frozen(value)
