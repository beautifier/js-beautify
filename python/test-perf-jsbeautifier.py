#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import copy
import jsbeautifier
options = jsbeautifier.default_options()
options.wrap_line_length = 80
data = ''
data_min = ''


def beautifier_test_underscore():
    jsbeautifier.beautify(data, options)


def beautifier_test_underscore_min():
    jsbeautifier.beautify(data_min, options)

def beautifier_test_github_min():
    jsbeautifier.beautify(github_min, options)


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
    underscore_file = os.path.join(
        dirname, "../", "test/resources/underscore.js")
    underscore_min_file = os.path.join(
        dirname, "../", "test/resources/underscore-min.js")
    github_min_file = os.path.join(
        dirname, "../", "test/resources/github-min.js")
    data = copy.copy(''.join(io.open(underscore_file, encoding="UTF-8").readlines()))
    data_min = copy.copy(''.join(io.open(underscore_min_file, encoding="UTF-8").readlines()))
    github_min = copy.copy(''.join(io.open(github_min_file, encoding="UTF-8").readlines()))

    # warm up
    beautifier_test_underscore()
    beautifier_test_underscore_min()
    beautifier_test_github_min()

    report_perf("beautifier_test_underscore")
    report_perf("beautifier_test_underscore_min")
    report_perf("beautifier_test_github_min")
