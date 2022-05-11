#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import re
import git
import sys
import getopt
import pathlib
import logging
import psycopg2
import subprocess
import svn.remote, svn.local

from .logger import *


VERSION_DELTA = [0, 0, 0, 1]

GIT_BRANCH = 'trunk'

PG_HOST = '192.168.1.127'
PG_DATABASE = 'version_control'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'

# default
valid_opts = {
    'force': False,
    'name': '',
    'detal_index': -1,
    'git_to_svn': False,
    'svn_remote': '',
    'svn_username': '',
    'svn_password': '',
}
valid_args = []

type_names = {
    '?': 'unversioned',
    '!': 'missing',
    'A': 'added',
    'C': 'conflicted',
    'D': 'deleted',
    'M': 'modified',
}


# CUSTOM
def calc_new_pg_version(old_pg_version, old_git_revision, old_svn_revision, new_git_revision, new_svn_revision):
    if old_pg_version is None:
        old_pg_version = [0, 0, 0, 0]

    new_pg_version = []
    for i in range(len(old_pg_version)):
        new_pg_version.append(old_pg_version[i] + VERSION_DELTA[i])
    return new_pg_version


def get_opts_and_args(argv):
    try:
        opts, args = getopt.getopt(argv, '', [
            'help',

            'force',
            'name=',
            'detal_index='
            
            'git_to_svn',
            'svn_remote=',
            'svn_username=',
            'svn_password=',
        ])
    except getopt.GetoptError:
        logging.error('getopt.GetoptError')
        sys.exit(-1)

    logging.info(opts)

    for opt, arg in opts:
        if opt in ('--help'):
            logging.info('?')
            exit(0)
        
        elif opt in ('--force'):
            valid_opts['force'] = True
        elif opt in ('--name'):
            valid_opts['name'] = arg
            valid_opts['table'] = arg
            valid_opts['file'] = os.path.join(arg, 'Properties', 'AssemblyInfo.cs')
        elif opt in ('--delta_index'):
            VERSION_DELTA[int(arg)] = 1
        
        elif opt in ('--git_to_svn'):
            valid_opts['git_to_svn'] = True
        elif opt in ('--svn_remote'):
            valid_opts['svn_remote'] = arg
        elif opt in ('--svn_username'):
            valid_opts['svn_username'] = arg
        elif opt in ('--svn_password'):
            valid_opts['svn_password'] = arg
        
        else:
            logging.warning('unknown opt: %s.' % opt)
    
    valid_args = args


class DemoVersionController(object):
    def __init__(self):
        pass

    def exe_cmd(self, cmd: str) -> str:
        logging.info(cmd)
        try:
            output = subprocess.check_output(cmd, shell=True)
        except:
            logging.error('Failure: %s' % cmd)
            exit(-1)

        try:
            result = '\n' + output.decode('gbk').replace('\r\n', '\n')
        except:
            result = '\n' + output.decode('utf-8')
        logging.info(result)
        return result


    def exe_sql(self, cur, sql):
        logging.info(sql)
        cur.execute(sql)
        try:
            rows = cur.fetchall()
        except:
            rows = None
        cur.close()
        return rows


    def connect_pg(self, host, database, user, password):
        self.conn = psycopg2.connect(host, database, user, password)


    def disconnect_pg(self):
        self.conn.close()


    def get_pg_version(self, table):
        sql = '''SELECT version, git_revision, svn_revision FROM public."%s" ORDER BY version DESC LIMIT 1;'''
        sql = sql % table
        rows = self.exe_sql(self.conn.cursor(), sql)

        row = rows[0]
        if row is not None:
            (pg_version, pg_git_revision, pg_svn_revision) = row
        else:
            (pg_version, pg_git_revision, pg_svn_revision) = (None, None, None)

        logging.info('pg_version: %s' % pg_version)
        logging.info('pg_git_revision: %s' % pg_git_revision)
        logging.info('pg_svn_revision: %s' % pg_svn_revision)

        self.old_pg_version = pg_version
        self.old_pg_git_revision = pg_git_revision
        self.old_pg_svn_revision = pg_svn_revision

        return (pg_version, pg_git_revision, pg_svn_revision)


    def get_git_revision(self, git_local_repo):
        git_revision = git_local_repo.head.commit.hexsha
        logging.info('git_revision: %s' % git_revision)
        return git_revision


    def get_git_not_ignored_paths(self, git_local_repo, path='.'):
        paths = []
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                cur_path = os.path.join(root, dir)
                cur_path_parts = pathlib.PureWindowsPath(cur_path).parts
                if '.git' not in cur_path_parts and '.svn' not in cur_path_parts:
                    paths.append(cur_path)
            for file in files:
                cur_path = os.path.join(root, file)
                cur_path_parts = pathlib.PureWindowsPath(cur_path).parts
                if '.git' not in cur_path_parts and '.svn' not in cur_path_parts:
                    paths.append(cur_path)

        git_ignored_paths = git_local_repo.ignored(paths)
        git_not_ignored_paths = [path for path in paths if path not in git_ignored_paths]
        return git_not_ignored_paths


    def get_git_msgs(self, git_local_repo, old_git_revision):
        git_msgs = []

        git_commits = list(git_local_repo.iter_commits(GIT_BRANCH, max_count=10))
        git_commits.reverse()

        logging.info('old_git_revision: %s' % old_git_revision)

        for git_commit in git_commits:
            cur_git_revision = git_commit.hexsha
            logging.info('cur_git_revision: %s %s' % (cur_git_revision, git_commit.message))

            if cur_git_revision != old_git_revision:
                git_msgs.append(git_commit.message)
            else:
                break

        git_msgs.reverse()
        return git_msgs


    def git_to_svn(self, git_local_repo, old_git_revision, svn_local_repo, old_svn_revision):
        git_not_ignored_paths = self.get_git_not_ignored_paths(git_local_repo)

        git_stash_flag = False
        cmd = 'git stash --include-untracked'
        result = self.exe_cmd(cmd)
        if result[1:-1] != 'No local changes to save':
            git_stash_flag = True

        cmd = 'svn status'
        result = self.exe_cmd(cmd)

        status = result[1:-1].split('\n')

        for item in status:
            type_name = type_names[item[0]]
            path = os.path.join('.', item[8:])
            logging.info('%s: %s' % (type_name, path))

            if path in git_not_ignored_paths:
                logging.info('path %s in git_not_ignored_paths' % path)

                if type_name == 'unversioned':
                    svn_local_repo.add(path)
                    if os.path.isdir(path):

                        if not os.path.exists(path):
                            logging.info('mkdir %s' % path)
                            os.mkdir(path)

                        subpaths = self.get_git_not_ignored_paths(git_local_repo, path=path)
                        for subpath in subpaths:
                            try:
                                svn_local_repo.add(subpath)
                            except Exception as e:
                                logging.warning(e)

                elif type_name == 'missing':
                    cmd = 'svn delete %s' % path
                    self.exe_cmd(cmd)

                else:
                    pass

        git_msgs = self.get_git_msgs(git_local_repo, old_git_revision)
        svn_msgs = '\n'.join(git_msgs)
        logging.info('\n' + svn_msgs)
        svn_local_repo.commit(svn_msgs)

        if git_stash_flag:
            cmd = 'git stash pop'
            self.exe_cmd(cmd)

        svn_local_repo.update()
        svn_revision = svn_local_repo.info()['commit_revision']

        return svn_revision


    def set_properties_assemblyinfo(self, filename, new_version):
        content = ''

        with open(filename, 'r', encoding='utf-8') as rf:
            content = rf.read()

        new_version_str = '.'.join([str(i) for i in new_version])
        content = re.sub('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', new_version_str, content)

        with open(filename, 'w', encoding='utf-8') as wf:
            wf.write(content)


    def set_pg_version(self, pg_version, git_revision, svn_revision):
        sql = '''INSERT INTO public."%s" (version, git_revision, svn_revision) VALUES (array%s, '%s', %d);'''
        sql = sql % (valid_opts['table'], pg_version, git_revision, svn_revision)
        self.exe_sql(self.conn.cursor(), sql)
        self.conn.commit()


    def run(self, force, table, file, git_to_svn, svn_remote, svn_username, svn_password, calc_new_pg_version):
        (old_pg_version, old_git_revision, old_svn_revision) = self.get_pg_version(table)

        git_local_repo = git.Repo('.')
        new_git_revision = self.get_git_revision(git_local_repo)
        logging.info('git_revision: %s' % new_git_revision)

        cmd = 'git stash clear'
        self.exe_cmd(cmd)

        cmd = 'git reset --hard %s' % new_git_revision
        self.exe_cmd(cmd)

        if git_to_svn and not os.path.exists('.svn'):
            cmd = 'svn checkout %s . --force --depth=infinity --username=%s --password=%s'
            cmd = cmd % (svn_remote, svn_username, svn_password)
            self.exe_cmd(cmd)
        svn_local_repo = svn.local.LocalClient('.', username=svn_username, password=svn_password)

        (new_pg_version, new_git_revision, new_svn_revision) = (None, None, None)
        if force or old_git_revision != new_git_revision:
            new_svn_revision = self.git_to_svn(git_local_repo, old_git_revision, svn_local_repo, old_svn_revision)
            new_pg_version = calc_new_pg_version(old_pg_version, old_git_revision, old_svn_revision, new_git_revision, new_svn_revision)
            self.set_properties_assemblyinfo(file, new_pg_version)
        else:
            self.set_properties_assemblyinfo(file, old_pg_version)

        return (new_pg_version, new_git_revision, new_svn_revision)


if __name__ == '__main__':
    logger = DemoLogger(file=False)

    get_opts_and_args(sys.argv[1:])
    version_controlller = DemoVersionController()
    version_controlller.connect_pg(PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD)
    (new_pg_version, new_git_revision, new_svn_revision) = version_controlller.run(
        valid_opts['force'],
        valid_opts['table'],
        valid_opts['file'],
        valid_opts['git_to_svn'],
        valid_opts['svn_remote'],
        valid_opts['svn_username'],
        valid_opts['svn_password'],
    )
    version_controlller.disconnect_pg()

    '''
    version_controlller = DemoVersionController()
    version_controlller.connect_pg(PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD)
    version_controlller.set_pg_version(new_pg_version, new_git_revision, new_svn_revision)
    version_controlller.disconnect_pg()
    '''