#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess


mkdir_lambda = lambda x: os.makedirs(x) if not os.path.exists(x) else True


class DemoTracter(object):
    def __init__(self):
        pass

    def contract(self, condir, archive = None, charset = 'utf-8'):
        ext = os.path.splitext(archive)[1][1:] if archive else 'zip'
        if ext == '' or not hasattr(self, 'contract_' + ext):
            return False
        arg_list, arg_dict = getattr(self, 'contract_' + ext)(condir, archive, charset)
        cmd = self.join_args(arg_list, arg_dict)
        print(cmd)
        if not cmd:
            return False
        if self.exe_cmd(cmd) != 0:
            return False
        return True

    def extract(self, archive, exdir = None, charset = 'utf-8'):
        ext = os.path.splitext(archive)[1][1:]
        if ext == '' or not hasattr(self, 'extract_' + ext):
            return False
        arg_list, arg_dict = getattr(self, 'extract_' + ext)(archive, exdir, charset)
        cmd = self.join_args(arg_list, arg_dict)
        print(cmd)
        if not cmd:
            return False
        if self.exe_cmd(cmd) != 0:
            return False
        self.merge_duplicate_exdir(exdir)
        return True

    def join_args(self, arg_list, arg_dict):
        cmd = []
        for arg in arg_list:
            if arg not in arg_dict or not arg_dict[arg]:
                continue

            if isinstance(arg, list):
                cmd.append(' '.join(arg_dict[arg]))
            elif isinstance(arg_dict[arg], dict):
                for k, v in arg_dict[arg].items():
                    cmd.append('%s %s' % (k, v))
            else:
                cmd.append(arg_dict[arg])
        return ' '.join(cmd)

    def exe_cmd(self, cmd):
        try:
            output = subprocess.check_output(cmd, shell = 'True', stderr = subprocess.STDOUT)
            returncode = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            returncode = e.returncode
        print(output.decode('utf-8'))
        return returncode

    def contract_rar(self, condir, archive, charset):
        arg_list = ['rar', 'commands', 'switches', 'archive', 'files', 'listfiles', 'path_to_extract']
        arg_dict = {
            'rar': 'rar',
            'commands': 'a',
            'archive': '"%s"' % archive if archive else condir + '.rar',
            'files': condir,
        }
        return arg_list, arg_dict

    def contract_zip(self, condir, archive, charset):
        arg_list = ['zip', 'options', 'path', 'mmddyyyy', 'suffixes', 'zipfile list', 'list']
        arg_dict = {
            'zip': 'zip',
            'options': '-r',
            'path': '%s' % archive,
            'zipfile list': condir,
        }
        return arg_list, arg_dict

    def extract_rar(self, archive, exdir, charset):
        arg_list = ['unrar', 'commands', 'switches', 'archive', 'files', 'listfiles', 'path_to_extract']
        arg_dict = {
            'unrar': 'unrar',
            'commands': 'x',
            'archive': '"%s"' % archive,
            'path_to_extract': exdir if exdir else ''
        }
        return arg_list, arg_dict

    def extract_zip(self, archive, exdir, charset):
        arg_list = ['unzip', 'modifiers', 'archive', 'list', 'xlist', 'exdir']
        arg_dict = {
            'unzip': 'unzip',
            'modifiers': {},
            'archive': '%s' % archive,
            'exdir': '-d %s' % exdir if exdir else '',
        }
        if charset != 'utf-8':
            arg_dict['modifiers']['-O'] = charset
        return arg_list, arg_dict

    def merge_duplicate_exdir(self, exdir):
        basename = os.path.basename(exdir)
        if os.path.isdir(exdir) and basename in os.listdir(exdir):
            index = 0 - len(basename)
            parentname = exdir[:index]
            if parentname == '':
                parentname = '.'
            exdir_copy = exdir + '_copy'
            os.rename(exdir, exdir_copy)
            shutil.move(os.path.join(exdir_copy, basename), parentname)
            shutil.rmtree(exdir_copy, ignore_errors = True)
