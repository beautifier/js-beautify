#!/usr/bin/env python

from distutils.core import setup

setup(name='jsbeautifier',
      version='1.0',
      description='JavaScript unobfuscator and beautifier.',
      long_description=('Beautify, unpack or deobfuscate JavaScript. '
                        'Handles popular online obfuscators.'),
      author='Einar Lielmanis, Stefano Sanfilippo et al.',
      author_email='einar@jsbeautifier.org',
      url='http://jsbeautifier.org',
      scripts=['js-beautify'],
      packages=['jsbeautifier', 'jsbeautifier.tests',
                'jsbeautifier.unpackers', 'jsbeautifier.unpackers.tests'],
      license='MIT',
     )
