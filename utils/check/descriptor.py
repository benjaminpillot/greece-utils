# -*- coding: utf-8 -*-

""" Descriptor classes

Use descriptor classes to implement data models
"""

# __all__ = []
# __version__ = '0.1'
__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2017, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'

# import


def lazyproperty(func):
    name = '_lazy_' + func.__name__

    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy


def protected_property(name):
    """ Protected property

    Function used for implementing
    repetitive "SetAccess = protected"
    of class properties
    :param name:
    :return:
    """
    storage_name = '_' + name

    @property
    def prop(self):
        return getattr(self, storage_name)

    return prop
