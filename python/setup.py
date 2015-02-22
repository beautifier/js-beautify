#!/usr/bin/env python

from distutils.core import setup
from jsbeautifier.__version__ import __version__

setup(name='jsbeautifier',
      version=__version__,
      description='JavaScript unobfuscator and beautifier.',
      long_description=('Beautify, unpack or deobfuscate JavaScript. '
                        'Handles popular online obfuscators.'),
      author='Einar Lielmanis, Stefano Sanfilippo et al.',
      author_email='einar@jsbeautifier.org',
      url='http://jsbeautifier.org',
      scripts=['js-beautify'],
      packages=['jsbeautifier', 'jsbeautifier.tests',
                'jsbeautifier.unpackers', 'jsbeautifier.unpackers.tests'],
      install_requires=["six>=1.6.1"],
      license='MIT',
     )
