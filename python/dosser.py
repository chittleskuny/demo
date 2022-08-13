#!/usr/bin/python
# -*- coding:utf-8 -*-

import getopt
import logging
import os
import re
import subprocess
import sys

from logger import *


class DemoDosser(object):
    def __init__(self):
        pass


    @staticmethod
    def get_opts(short_opts, long_opts, argv=None):
        valid_opts, valid_args = {}, {}

        if argv is None:
            if len(sys.argv) < 1:
                logging.error('No argv!') 
                exit(-1)
            else:
                argv = sys.argv[1:]

        try:
            opts, args = getopt.getopt(argv, short_opts, long_opts)
        except getopt.GetoptError as e:
            logging.error(e)
            sys.exit(-1)

        for opt, arg in opts:
            if opt.startswith('-'):
                pass # Not Support yet.
            if opt.startswith('--'):
                opt = opt[2:]
                if opt in long_opts:
                    valid_opts[opt] = True
                elif opt + '=' in long_opts:
                    valid_opts[opt] = arg
                else:
                    logging.warning(opt)
        
        valid_args = args

        return (valid_opts, valid_args)


    @staticmethod
    def exe(cmd):
        cmd = cmd.replace('    ', '')
        logging.info(cmd)
        try:
            output = subprocess.check_output(cmd, shell=True)
        except:
            logging.error('The command execution failure: %s' % cmd)
            exit(-1)
        result = '\n' + output.decode('gbk').replace('\r\n', '\n')
        logging.info(result)
        return result


    @staticmethod
    def tree(output):
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
                    path_stack, tail_stack = DemoDosser._pop(path_stack, tail_stack)
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
                    path_stack, tail_stack = DemoDosser._pop(path_stack, tail_stack)
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
                    path_stack, tail_stack = DemoDosser._pop(path_stack, tail_stack)

            else:
                pass

        return tree_list


    @staticmethod
    def _pop(path_stack, tail_stack):
        while tail_stack and tail_stack[-1] == 1:
            path_stack.pop()
            tail_stack.pop()
        if len(tail_stack) > 0 and tail_stack[-1] != 0:
            path_stack.pop()
            tail_stack.pop()
        return path_stack, tail_stack


    @staticmethod
    def scp(source, target, skip=False):
        if DemoDosser._scp_test(source):
            cmd = 'scp %s %s' % (source, target)
            DemoDosser.exe(cmd)
            return True
        elif skip:
            return False
        else:
            exit(-1)


    @staticmethod
    def _scp_test(path_file):
        index = path_file.find(':')
        if index != -1:
            _prefix = path_file[:index]
            _suffix = path_file[(index + 1):]

            test_cmd = 'ssh %s "ls %s > /dev/null 2>&1"' % (_prefix, _suffix)
            logging.info(test_cmd)
            try:
                output = subprocess.check_output(test_cmd, shell=True)            
            except:
                logging.error('No such file: %s' % path_file)
                return False
            result = '\n' + output.decode('gbk').replace('\r\n', '\n')
            logging.info(result)
            return True
        else:
            if not os.path.exists(path_file):
                logging.error('No such file: %s' % path_file)
                return False
            else:
                return True


    @staticmethod
    def wmic_datafile_get_version(debug_flag, filename):
        release_filename = os.path.join('Release', filename)
        if debug_flag:
            release_filename = os.path.join('Debug', filename)
        if not os.path.isfile(release_filename):
            logging.error('File %s not found!' % filename)
            exit(-1)
        
        abspath = os.path.abspath(release_filename)
        abspath = abspath.replace('\\', '\\\\')
        cmd = r'''wmic datafile where "name='%s'" get Version''' % abspath
        output = DemoDosser.exe(cmd)
        lines = output.split()

        numbers = [0, 0, 0, 0]
        for line in lines:
            m = re.match('([\d]+)\.([\d]+)\.([\d]+)(\.([\d]+))?', line)
            if m:
                groups = m.groups()
                numbers[0] = int(groups[0])
                numbers[1] = int(groups[1])
                numbers[2] = int(groups[2])
                if groups[4] is not None:
                    numbers[3] = int(groups[4])
                break
        return numbers


if __name__ == '__main__':

    DemoLogger(file_enable=False)

    # DemoDosser get_opts

    short_opts = ''
    long_opts = [
        'help',
        'arg_a',
        'opt_b=',
        'opt_c=',
    ]
    argv = [
        '--arg_a',
        '--opt_b=bb',
        '--opt_c=cc',
    ]
    (valid_opts, valid_args) = DemoDosser.get_opts(short_opts, long_opts, argv)
    logging.info(valid_opts)
    logging.info(valid_args)

    # DemoDosser exe

    cmd = '''
        echo %date%
    '''
    DemoDosser.exe(cmd)
