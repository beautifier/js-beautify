#!/usr/bin/env python

import os
import sys

from setup import PyTest  # from setyp.py, not setuptools!

from setuptools import setup
from jsbeautifier.__version__ import __version__

from setuptools.command.test import test as TestCommand

DIR_CSS = "cssbeautifier/tests/"


class PyTestCSS(PyTest):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["--assert=plain"] + [
            DIR_CSS + x
            for x in os.listdir(DIR_CSS)
            if x.endswith(".py") and x[0] not in "._"
        ]


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
    test_suite="pytest.collector",
    cmdclass={"test": PyTestCSS},
)
