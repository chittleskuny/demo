#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys

from cat import *
from database_administrator import *
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


    def test_demo_cat(self):
        cat = DemoCat(True)
        cat._tail('cat.py')


    def test_demo_excel(self):
        xls = DemoExcel('test.xls')
        xls.open_worksheet('test')
        xls.save_workbook()

        xlsx = DemoExcel('test.xlsx')
        xlsx.open_worksheet('test')
        xlsx.save_workbook()


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
