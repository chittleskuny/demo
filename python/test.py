#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

from logger import *


class DemoTest(object):
    def __init__(self):
        pass

    def test(self, case):
        if hasattr(self, 'test_demo_' + case):
            getattr(self, 'test_demo_' + case)()
        else:
            pass


if __name__ == '__main__':
    if len(sys.argv) < 1:
        exit(1)

    test = DemoTest()
    case = sys.argv[1]
    test.test(case)
