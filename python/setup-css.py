#!/usr/bin/env python

import os
import sys

from setuptools import setup
from jsbeautifier.__version__ import __version__

import testcommand
from testcommand import PyTest, DIR

testcommand.DIR = 'cssbeautifier/tests/'

setup(name='cssbeautifier',
      version=__version__,
      description='CSS unobfuscator and beautifier.',
      long_description=('Beautify, unpack or deobfuscate CSS'),
      author='Liam Newman, Einar Lielmanis, et al.',
      author_email='team@beautifier.io',
      url='https://beautifier.io',
      entry_points={
          'console_scripts': [
              'css-beautify = cssbeautifier:main'
          ]
      },
      packages=['cssbeautifier',
                'cssbeautifier.tests', 'cssbeautifier.tests.generated',
                'cssbeautifier.css'],
      install_requires=["jsbeautifier>=__version__",
                        "six>=1.13.0",
                        "editorconfig>=0.12.2"],
      license='MIT',
      test_suite='pytest.collector',
      cmdclass={'test': PyTest},

      )
