#!/usr/bin/env python

import os,sys

from setuptools import setup
from jsbeautifier.__version__ import __version__

from setuptools.command.test import test as TestCommand

DIR='jsbeautifier/tests/'
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--assert=plain'] +[DIR+x for x in os.listdir(DIR) if x.endswith('.py') and x[0] not in '._']

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(name='jsbeautifier',
      version=__version__,
      description='JavaScript unobfuscator and beautifier.',
      long_description=('Beautify, unpack or deobfuscate JavaScript. '
                        'Handles popular online obfuscators.'),
      author='Einar Lielmanis, Stefano Sanfilippo et al.',
      author_email='einar@jsbeautifier.org',
      url='http://jsbeautifier.org',
      scripts=['js-beautify'],
      packages=['jsbeautifier', 'jsbeautifier.tests', 'jsbeautifier.tests.generated',
                'jsbeautifier.unpackers', 'jsbeautifier.unpackers.tests'],
      install_requires=["six>=1.6.1", "editorconfig>=0.12.0"],
      license='MIT',
      test_suite='pytest.collector',
      cmdclass = {'test': PyTest},

     )
