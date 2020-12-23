#!/usr/bin/env python

import os
import sys

from setuptools import setup
from cssbeautifier.__version__ import __version__

from setuptools.command.test import test as TestCommand

DIR_CSS = "cssbeautifier/tests/"


class PyTestCSS(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["--assert=plain"] + [
            DIR + x for x in os.listdir(DIR) if x.endswith(".py") and x[0] not in "._"
        ]

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


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
