#!/usr/bin/python3
# -*- coding:utf-8 -*-

class DemoStepper(object):
    def __init__(self):
        self.max = [] # number list
        self.cur = [] # number list

    def __str__(self):
        template_item = '[%d/%d]'
        template_list = []
        if len(self.max) > 0:
            for i in range(len(self.max)):
                template_list.append(template_item % (self.cur[i], self.max[i]))
        return ''.join(template_list)

    def append(self, steps):
        self.max.append(len(steps))
        self.cur.append(0)
        return 0

    def next(self):
        for i in range(len(self.max) - 1, -1, -1):
            if self.cur[i] < self.max[i]:
                self.cur[i] = self.cur[i] + 1
                return 0
            else: # self.cur[i] = self.max[i]
                self.cur.pop()
                self.max.pop()
        return 0
