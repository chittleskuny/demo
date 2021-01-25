#!/usr/bin/python3
# -*- coding:utf-8 -*-


class DemoStepper(object):
    def __init__(self, mode='both'):
        self.max, self.cur = [], [] # number list
        self.limit_from, self.limit_to = None, None
        self.mode = mode
        self.flag = False

    def __str__(self):
        percent_unit = 100
        percent = 0
        fraction_item = '[%d/%d]'
        fraction_list = []
        if len(self.max) > 0:
            for i in range(len(self.max)):
                percent_unit = percent_unit/self.max[i]
                percent = percent + (self.cur[i] - 1)*percent_unit
                fraction_list.append(fraction_item % (self.cur[i], self.max[i]))
        if self.flag:
            percent = percent + percent_unit
        step = ""
        if self.mode == 'percent':
            step = '[' + '%.2f' % percent + '%] '
        elif self.mode == 'fraction':
            step = ''.join(fraction_list) + ' '
        else:
            step = '[' + '%.2f' % percent + '%] ' + ''.join(fraction_list) + ' '
        return step

    def append(self, steps):
        self.max.append(len(steps))
        self.cur.append(0)
        return 0

    def limit(self, limit_from=None, limit_to=None):
        if limit_from:
            self.limit_from = list(map(lambda x:int(x), limit_from))
        if limit_to:
            self.limit_to = list(map(lambda x:int(x), limit_to))
        return True

    def check(self):
        if self.limit_from:
            for i in range(len(self.limit_from)):
                if len(self.cur) > i and self.cur[i] < self.limit_from[i]:
                    return -1
        if self.limit_to:
            for i in range(len(self.limit_to)):
                if len(self.cur) > i and self.cur[i] > self.limit_to[i]:
                    return 1
        return 0

    def next(self):
        self.flag = False
        for i in range(len(self.max) - 1, -1, -1):
            if self.cur[i] < self.max[i]:
                self.cur[i] = self.cur[i] + 1
                return 0
            else: # self.cur[i] = self.max[i]
                self.cur.pop()
                self.max.pop()
        return 0

    def commit(self):
        self.flag = True
