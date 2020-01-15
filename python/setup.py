#!/usr/bin/env python

import os
import sys

from setuptools import setup
from jsbeautifier.__version__ import __version__

import testcommand
from testcommand import PyTest

testcommand.DIR = 'jsbeautifier/tests/'

setup(name='jsbeautifier',
      version=__version__,
      description='JavaScript unobfuscator and beautifier.',
      long_description=('Beautify, unpack or deobfuscate JavaScript. '
                        'Handles popular online obfuscators.'),
      author='Liam Newman, Einar Lielmanis, et al.',
      author_email='team@beautifier.io',
      url='https://beautifier.io',
      entry_points={
          'console_scripts': [
              'js-beautify = jsbeautifier:main'
          ]
      },
      packages=['jsbeautifier',
                'jsbeautifier.tests', 'jsbeautifier.tests.generated',
                'jsbeautifier.core',
                'jsbeautifier.javascript',
                'jsbeautifier.unpackers', 'jsbeautifier.unpackers.tests'],
      install_requires=["six>=1.13.0", "editorconfig>=0.12.2"],
      license='MIT',
      test_suite='pytest.collector',
      cmdclass={'test': PyTest},

      )
