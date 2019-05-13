# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

__version__ = '0.1'
__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'


from setuptools import setup, find_packages

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(name='greece-utils',
      version='0.1.0',
      description='GREECE utils',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/benjamin-pillot/greece-utils',
      author='Benjamin Pillot',
      author_email='benjaminpillot@riseup.net',
      license='GNU GPL v3.0',
      packages=find_packages(),
      zip_safe=False)
