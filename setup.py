#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

__version__ = '0.0.1'

setup(
    name = 'pypacian',
    version = __version__,
    description = 'Packet Editing Tool for Python',
    long_description = '''
    PyPacian a packet capturing, editing, ad senfing tool for Python
    ''',
    author = 'Shin Kurita',
    url = 'https://github.com/montblanc18',
    license = 'GPLv2',
    install_package_data = True,
    package_dir = {'input':'input',},
    packages = find_packages(exclude = ('tests', 'docs')),
    package_data = {'input':['input'],},
    install_requires = ['setuptools', 'scapy', 'PyX'],
    test_suite = 'tests'
)
