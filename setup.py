#!/usr/bin/env python
from distutils.version import LooseVersion
import os
import pip
from setuptools import find_packages
from setuptools import setup
import sys


if LooseVersion(sys.version) < LooseVersion('3.6'):
    raise RuntimeError(
        'LocataWrapper requires Python>=3.6, '
        'but your Python is {}'.format(sys.version))
if LooseVersion(pip.__version__) < LooseVersion('19'):
    raise RuntimeError(
        'pip>=19.0.0 is required, but your pip is {}. '
        'Try again after "pip install -U pip"'.format(pip.__version__))

requirements = {
    'install': [
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
    'setup': ['numpy', 'pytest-runner'],
    'test': [
        'ipdb',
        'pytest>=3.3.0',
        'pytest-pythonpath>=0.7.3',
        'pytest-cov>=2.7.1',
        'hacking>=1.1.0',
        'mock>=2.0.0',
        'autopep8>=1.3.3',
        'jsondiff']}
install_requires = requirements['install']
setup_requires = requirements['setup']
tests_require = requirements['test']
extras_require = {k: v for k, v in requirements.items()
                  if k not in ['install', 'setup']}

dirname = os.path.dirname(__file__)
setup(name='locata_wrapper',
      version='0.1.0',
      url='http://github.com/Fhrozen/locata_python',
      author='Nelson Yalta',
      author_email='nyalta21@gmail.com',
      description='Locata Wrapper: Tools for LOCATA Challenge in Python',
      long_description=open(os.path.join(dirname, 'README.md'),
                            encoding='utf-8').read(),
      license='Apache Software License',
      packages=find_packages(include=['locata_wrapper*']),
      install_requires=install_requires,
      setup_requires=setup_requires,
      tests_require=tests_require,
      extras_require=extras_require,
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Science/Research',
          'Operating System :: POSIX :: Linux',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      )