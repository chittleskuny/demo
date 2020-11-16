#!/usr/bin/python
# -*- coding:utf-8 -*-


import os
import sys

from dosser import *
from excel import *
from logger import *
from stepper import *
from tracter import *


class DemoTest(object):
    def __init__(self):
        pass

    def test(self, case):
        if hasattr(self, 'test_demo_' + case):
            getattr(self, 'test_demo_' + case)()
        else:
            print('No such case %s.' % case)

    def test_demo_dosser(self):
        dosser = DemoDosser()
        tree_list = dosser.tree('output.txt')
        print(tree_list)

    def test_demo_excel(self):
        xls = DemoExcel('test.xls')
        xls.open_worksheet('test')
        xls.save_workbook()

        xlsx = DemoExcel('test.xlsx')
        xlsx.open_worksheet('test')
        xlsx.save_workbook()

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

    def test_demo_stepper(self):
        stepper = DemoStepper()
        steps = [
            'step_1',
            'step_2',
            'step_3',
        ]
        stepper.append(steps)
        stepper.next()
        print(str(stepper))
        stepper.next()
        print(str(stepper))
        stepper.next()
        print(str(stepper))

    def test_demo_tracter(self):
        tracter = DemoTracter()
        os.system('''
            mkdir -p ~/test/tracter/src;
            echo "abc" > ~/test/tracter/src/abc.txt;
            echo "def" > ~/test/tracter/src/def.txt;
        ''')
        if tracter.contract('~/test/tracter/src', '~/test/tracter/src.zip'):
            os.system('rm -rf ~/test/tracter/src')
            tracter.extract('~/test/tracter/src.zip', '~/test/tracter/src')


if __name__ == '__main__':
    if len(sys.argv) < 1:
        exit(1)

    test = DemoTest()
    case = sys.argv[1]
    test.test(case)
