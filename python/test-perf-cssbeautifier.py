#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import copy
import cssbeautifier
options = cssbeautifier.default_options()
options.wrap_line_length = 80
data = ''


def beautifier_test_github_css():
    cssbeautifier.beautify(data, options)


def report_perf(fn):
    import timeit
    iter = 5
    time = timeit.timeit(
        fn +
        "()",
        setup="from __main__ import " +
        fn +
        "; gc.enable()",
        number=iter)
    print(fn + ": " + str(iter / time) + " cycles/sec")


if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(__file__))
    github_file = os.path.join(
        dirname, "../", "test/resources/github.css")
    data = copy.copy(''.join(io.open(github_file).readlines()))

    # warm up
    beautifier_test_github_css()

    report_perf("beautifier_test_github_css")
