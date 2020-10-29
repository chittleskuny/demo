#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import os


class DemoDosser(object):
    def __init__(self):
        pass

    def tree(self, output):
        with open(output, 'r') as f:
            lines = f.readlines()

        tree_list = []

        path_stack, tail_stack = [], []
        last_tab, last_span = 0, 0
        tail_branch_test, tail_branch_flag = False, False

        for line_no, line in enumerate(lines):
            if line_no == 0 or line_no == 1:
                pass

            elif line_no == 2:
                volume = line[0:2]
                path_stack.append(volume)
                tail_stack.append(0)

            elif re.match('[ │]*└─', line):
                span = re.match('[ │]*└─', line).span()
                if span == last_span and tail_branch_test:
                    path_stack.pop()
                    tail_stack.pop()
                if last_tab == 1 and last_span[1] > span[1]:
                    path_stack, tail_stack = self._pop(path_stack, tail_stack)
                last_tab, last_span = 1, span
                tail_branch_test = True
                pathname = line[span[1]:-1]
                path_stack.append(pathname)
                tail_stack.append(1)
                tree_list.append(os.path.join(*path_stack))

            elif re.match('[ │]*├─', line):
                span = re.match('[ │]*├─', line).span()
                if span == last_span and tail_branch_test:
                    path_stack.pop()
                    tail_stack.pop()
                if last_tab == 1 and last_span[1] > span[1]:
                    path_stack, tail_stack = self._pop(path_stack, tail_stack)
                last_tab, last_span = 2, span
                tail_branch_test = True
                pathname = line[span[1]:-1]
                path_stack.append(pathname)
                tail_stack.append(2)
                tree_list.append(os.path.join(*path_stack))

            elif re.match('[ │]*', line):
                span = re.match('[ │]*', line).span()
                last_tab, last_span = 3, span
                filename = line[span[1]:-1]
                if filename:
                    if tail_branch_test and line[span[1] - 3] == '│':
                        tail_branch_flag = True
                    tree_list.append(os.path.join(*path_stack, filename))
                else:
                    if tail_branch_flag:
                        tail_branch_test, tail_branch_flag = False, False
                        continue
                    path_stack, tail_stack = self._pop(path_stack, tail_stack)

            else:
                pass

        return tree_list

    def _pop(self, path_stack, tail_stack):
        while tail_stack and tail_stack[-1] == 1:
            path_stack.pop()
            tail_stack.pop()
        if len(tail_stack) > 0 and tail_stack[-1] != 0:
            path_stack.pop()
            tail_stack.pop()
        return path_stack, tail_stack
