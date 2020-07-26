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

    def test_demo_logger(self):
        DemoLogger()
        logging.debug('A')

        '''
        A
        '''

    def test_demo_logger_tree(self):
        DemoLoggerTree()
        logging.debug('A')

        logger_lv0 = logging.getLogger()
        logger_lv1 = logging.getLogger('Lv1')
        logger_lv2 = logging.getLogger('Lv1.Lv2')
        logger_lv0.debug('B')
        logger_lv1.debug('C')
        logger_lv2.debug('D')

        '''
        [0] A
        [0] B
        [1] C
        [0] C
        [2] D
        [1] D
        [0] D
        '''

if __name__ == '__main__':
    if len(sys.argv) < 1:
        exit(1)

    test = DemoTest()
    case = sys.argv[1]
    test.test(case)
