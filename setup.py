"""Setuptools for Locata Wrapper.
"""

#!/usr/bin/env python
from distutils.version import LooseVersion
from os import path
import pip
from setuptools import find_packages
from setuptools import setup
import sys


mainpath = path.abspath(path.dirname(__file__))
with open(path.join(mainpath, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = 'locata_wrapper',
    version = '0.1.0',
    description = 'Locata Wrapper: Tools for LOCATA Challenge in Python',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'http://github.com/audiofhrozen/locata_python',
    author = 'Nelson Yalta',
    author_email = 'nyalta21@gmail.com',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages = find_packages(include = ['locata_wrapper*']),
    python_requires= '>=3.6',
    install_requires = [
        'librosa',
        'pandas>=0.24.0',
        'pathos>=0.2.0',
        'pymongo>=3.0.0',
        'python_speech_features>=0.6',
        'setuptools>=38.5.1',
        'sacred>=0.7.0',
        'scipy',
        'soundfile>=0.10.2',
        'PyYAML',
    ],
    setup_requires = [
        'numpy', 'pytest-runner'
    ],
    extras_require = {
        'test': [
        'ipdb',
        'pytest>=3.3.0',
        'pytest-pythonpath>=0.7.3',
        'pytest-cov>=2.7.1',
        'hacking>=1.1.0',
        'mock>=2.0.0',
        'autopep8>=1.3.3',
        'jsondiff'
    ]},
    # package_data={
    #     'sample': ['package_data.dat'],
    # }
    license='Apache Software License',
)
