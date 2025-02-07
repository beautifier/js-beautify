#!/usr/bin/env python

from setuptools import setup
from cssbeautifier.__version__ import __version__


setup(
    name="cssbeautifier",
    version=__version__,
    description="CSS unobfuscator and beautifier.",
    long_description=("Beautify, unpack or deobfuscate CSS"),
    author="Liam Newman, Einar Lielmanis, et al.",
    author_email="team@beautifier.io",
    url="https://beautifier.io",
    entry_points={"console_scripts": ["css-beautify = cssbeautifier:main"]},
    packages=[
        "cssbeautifier",
        "cssbeautifier.tests",
        "cssbeautifier.tests.generated",
        "cssbeautifier.css",
    ],
    install_requires=["jsbeautifier", "six>=1.13.0", "editorconfig>=0.12.2"],
    license="MIT",
)
