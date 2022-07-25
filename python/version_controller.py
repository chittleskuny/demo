#!/usr/bin/python
# -*- coding:utf-8 -*-

import getopt
import git
import logging
import os
import pathlib
import re
import shutil
import svn.remote, svn.local
import sys

from database_administrator import *
from dosser import *
from logger import *


# default
properties = {
    'Configuration': 'Release',
    'Platform': 'AnyCPU',
}

valid_opts = {
    'config': None,
    'service': None,
    'root_directory': '.',
    'name': None,
    'mini_releases': None,
    'properties': properties,
    'start_index': 3,
    'delta_index': -1,
    'git_branch': 'master',
    'git_to_svn': False,
    'force': False,
    'svn_remote': None,
    'svn_username': None,
    'svn_password': None,
    'pg_version': None,
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


def get_opts_and_args(argv):
    try:
        opts, args = getopt.getopt(argv, '', [
            'help',
            'config=',
            'service=',
            'root_directory='
            'name=',
            'mini_releases=',
            'start_index=',
            'delta_index=',
            'git_branch=',
            'git_to_svn',
            'force',
            'svn_remote=',
            'svn_username=',
            'svn_password=',
            'pg_version=',
        ])
    except getopt.GetoptError as e:
        logging.error(e)
        sys.exit(-1)

    for opt, arg in opts:
        if opt in ('--help'):
            logging.info('?')
            exit(0)
        elif opt in ('--config'):
            valid_opts['config'] = arg
        elif opt in ('--service'):
            valid_opts['service'] = arg
        elif opt in ('--root_directory'):
            valid_opts['root_directory'] = arg
        elif opt in ('--name'):
            valid_opts['name'] = arg
        elif opt in ('--mini_releases'):
            valid_opts['mini_releases'] = arg
        elif opt in ('--start_index'):
            valid_opts['start_index'] = int(arg)
        elif opt in ('--delta_index'):
            valid_opts['delta_index'] = int(arg)
        elif opt in ('--git_branch'):
            valid_opts['git_branch'] = arg
        elif opt in ('--git_to_svn'):
            valid_opts['git_to_svn'] = True
        elif opt in ('--force'):
            valid_opts['force'] = True
        elif opt in ('--svn_remote'):
            valid_opts['svn_remote'] = arg
        elif opt in ('--svn_username'):
            valid_opts['svn_username'] = arg
        elif opt in ('--svn_password'):
            valid_opts['svn_password'] = arg
        elif opt in ('--pg_version') and arg != '':
            valid_opts['pg_version'] = [int(i) for i in arg.split('.')]
        else:
            logging.warning('unknown opt: %s.' % opt)
    
    logging.info('config: %s' % valid_opts['config'])
    logging.info('service: %s' % valid_opts['service'])
    logging.info('root_directory: %s' % valid_opts['root_directory'])
    logging.info('name: %s' % valid_opts['name'])
    logging.info('mini_releases: %s' % valid_opts['mini_releases'])
    logging.info('start_index: %s' % valid_opts['start_index'])
    logging.info('delta_index: %s' % valid_opts['delta_index'])
    logging.info('git_branch: %s' % valid_opts['git_branch'])
    logging.info('git_to_svn: %s' % valid_opts['git_to_svn'])
    logging.info('force: %s' % valid_opts['force'])
    logging.info('svn_remote: %s' % valid_opts['svn_remote'])
    logging.info('svn_username: %s' % valid_opts['svn_username'])
    logging.info('svn_password: %s' % valid_opts['svn_password'])
    logging.info('pg_version: %s' % valid_opts['pg_version'])

    valid_args = args
    logging.info('valid_args: %s' % valid_args)


class DemoVersionController(object):
    def __init__(
            self,
            name,
            mini_releases,
            start_index,
            delta_index,
            git_branch='master',
            git_to_svn=False,
            force=False,
            svn_remote=None,
            svn_username=None,
            svn_password=None,
            pg_version=None
        ):
        self.name = name

        self.start_version = [
            [1],
            [1, 0],
            [1, 0, 0],
            [1, 0, 0, 0],
        ][start_index]
        self.delta_version = [
            [1],
            [0, 1],
            [0, 0, 1],
            [0, 0, 0, 1],
        ][delta_index]

        self.git_local_repo = git.Repo('.')
        self.git_branch = git_branch

        self.git_to_svn = git_to_svn
        self.svn_local_repo = None
        self.force = force

        if self.git_to_svn:

            if not os.path.exists('.svn'):
                cmd = 'svn checkout %s . --force --depth=infinity --username=%s --password=%s'
                cmd = cmd % (svn_remote, svn_username, svn_password)
                DemoDosser.exe(cmd)
            
            self.svn_local_repo = svn.local.LocalClient('.', username=svn_username, password=svn_password)

        self.pg_version = pg_version
        if pg_version is not None:
            self.git_to_svn = False
            self.force = False


    def exe_sql(self, sql):
        cur = self.conn.cursor()

        logging.info(sql)
        cur.execute(sql)
        try:
            rows = cur.fetchall()
        except:
            rows = None

        cur.close()
        return rows


    def connect_pg(self, connection):
        self.conn = connection


    def disconnect_pg(self):
        self.conn.close()


    def get_pg_version(self):
        (pg_version, pg_git_revision, pg_svn_revision) = (None, None, None)

        if not self.git_to_svn:
            sql = '''SELECT version, git_revision FROM public."%s" ORDER BY version DESC LIMIT 1;'''
            sql = sql % self.name
            rows = self.exe_sql(sql)

            if not rows:
                pg_version = None
            else:
                (pg_version, pg_git_revision) = rows[0]

        else:
            sql = '''SELECT version, git_revision, svn_revision FROM public."%s" ORDER BY version DESC LIMIT 1;'''
            sql = sql % self.name
            rows = self.exe_sql(sql)

            if not rows:
                pg_version = None
            else:
                (pg_version, pg_git_revision, pg_svn_revision) = rows[0]
        
        logging.info('pg_version: %s' % pg_version)
        logging.info('pg_git_revision: %s' % pg_git_revision)
        logging.info('pg_svn_revision: %s' % pg_svn_revision)

        return (pg_version, pg_git_revision, pg_svn_revision)


    def get_git_revision(self):
        cmd = 'git reset --hard'

        if self.pg_version is not None:

            sql = '''
                SELECT git_revision FROM public."%s" WHERE version = array%s
            '''.replace('    ', '')
            sql = sql % (self.name, self.pg_version)
            rows = self.exe_sql(sql)
            if rows is None:
                exit(-1)

            git_revision = rows[0][0]
            cmd = 'git reset --hard ' + git_revision

        DemoDosser.exe(cmd)

        git_revision = self.git_local_repo.head.commit.hexsha
        logging.info('git_revision: %s' % git_revision)
        return git_revision


    def get_git_not_ignored_paths(self, path='.'):
        git_not_ignored_paths = []
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                cur_path = os.path.join(root, dir)
                cur_path_parts = pathlib.PureWindowsPath(cur_path).parts
                if '.git' not in cur_path_parts and '.svn' not in cur_path_parts:
                    if not self.git_local_repo.ignored([cur_path]):
                        git_not_ignored_paths.append(cur_path)
            for file in files:
                cur_path = os.path.join(root, file)
                cur_path_parts = pathlib.PureWindowsPath(cur_path).parts
                if '.git' not in cur_path_parts and '.svn' not in cur_path_parts:
                    if not self.git_local_repo.ignored([cur_path]):
                        git_not_ignored_paths.append(cur_path)
        return git_not_ignored_paths


    def get_git_msgs(self, old_git_revision):
        git_msgs = []

        git_commits = list(self.git_local_repo.iter_commits(self.git_branch, max_count=100))
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


    def commit_git_to_svn(self, old_git_revision, old_svn_revision):
        git_not_ignored_paths = self.get_git_not_ignored_paths()

        git_stash_flag = False
        cmd = 'git stash --include-untracked'
        result = DemoDosser.exe(cmd)
        if result[1:-1] != 'No local changes to save':
            git_stash_flag = True

        try:

            cmd = 'svn status'
            result = DemoDosser.exe(cmd)

            status = result[1:-1].split('\n')

            for item in status:
                type_name = type_names[item[0]]
                path = os.path.join('.', item[8:])
                logging.info('%s: %s' % (type_name, path))

                if path in git_not_ignored_paths:
                    logging.info('path %s in git_not_ignored_paths' % path)

                    if type_name == 'unversioned':
                        self.svn_local_repo.add(path)
                        if os.path.isdir(path):

                            if not os.path.exists(path):
                                logging.info('mkdir %s' % path)
                                os.mkdir(path)

                            subpaths = self.get_git_not_ignored_paths(path=path)
                            for subpath in subpaths:
                                try:
                                    self.svn_local_repo.add(subpath)
                                except Exception as e:
                                    logging.warning(e)

                    elif type_name == 'missing':
                        cmd = 'svn delete %s' % path
                        DemoDosser.exe(cmd)

                    else:
                        pass

            git_msgs = self.get_git_msgs(old_git_revision)
            svn_msgs = '\n'.join(git_msgs)
            logging.info('\n' + svn_msgs)
            self.svn_local_repo.commit(svn_msgs)

        except:

            logging.error('git to svn commit failed.')

        finally:

            if git_stash_flag:
                cmd = 'git stash pop'
                DemoDosser.exe(cmd)

        self.svn_local_repo.update()
        new_svn_revision = self.svn_local_repo.info()['commit_revision']

        return new_svn_revision


    def set_properties_assembly_info(self, new_pg_version_str):
        properties['ProductVersion'] = new_pg_version_str
        properties['AssemblyVersion'] = new_pg_version_str
        properties['AssemblyFileVersion'] = new_pg_version_str

        assembly_info = None
        if os.path.exists(os.path.join(self.name, 'Properties', 'AssemblyInfo.cs')):
            assembly_info = os.path.join(self.name, 'Properties', 'AssemblyInfo.cs')
        if os.path.exists(os.path.join(self.name, 'AssemblyInfo.cs')):
            assembly_info = os.path.join(self.name, 'AssemblyInfo.cs')
        
        if assembly_info is not None:

            content = ''
            with open(assembly_info, 'r', encoding='utf-8') as rf:
                content = rf.read()

            content = re.sub('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', new_pg_version_str, content)

            with open(assembly_info, 'w', encoding='utf-8') as wf:
                wf.write(content)


    def set_pg_version(self, pg_version_str, git_revision, svn_revision):
        pg_version_str = pg_version_str.replace('.', ',')

        sql = ''
        if svn_revision is None:
            sql = '''
                INSERT INTO public."%s" (version, git_revision) VALUES (array[%s], '%s')
                ON CONFLICT(version) DO UPDATE SET git_revision = '%s';
            '''.replace('    ', '')
            sql = sql % (self.name, pg_version_str, git_revision, git_revision)
        else:
            sql = '''
                INSERT INTO public."%s" (version, git_revision, svn_revision) VALUES (array[%s], '%s', %d)
                ON CONFLICT(version) DO UPDATE SET git_revision = '%s', svn_revision = %d;
            '''.replace('    ', '')
            sql = sql % (self.name, pg_version_str, git_revision, svn_revision, git_revision, svn_revision)
        self.exe_sql(sql)
        self.conn.commit()


    def calc_new_pg_version(self, old_pg_version, old_git_revision, old_svn_revision, new_git_revision, new_svn_revision):
        if self.pg_version is not None:
            return self.pg_version

        new_pg_version = []
        if old_pg_version is None:
            new_pg_version = self.start_version
        elif old_git_revision == new_git_revision:
            new_pg_version = old_pg_version
        else:
            
            update = False
            for i in range(len(old_pg_version)):
                if not update:
                    new_pg_version.append(old_pg_version[i] + self.delta_version[i])
                    if self.delta_version[i] != 0:
                        update = True
                else:
                    new_pg_version.append(0)


        logging.info('pg_version: %s -> %s' % (old_pg_version, new_pg_version))
        logging.info('git_revision: %s -> %s' % (old_git_revision, new_git_revision))
        logging.info('svn_revision: %s -> %s' % (old_svn_revision, new_svn_revision))

        return new_pg_version


    def run(self, properties):
        (new_pg_version_str, new_git_revision, new_svn_revision) = self.run_before_build()
        self.build(properties)
        self.run_after_build(new_pg_version_str, new_git_revision, new_svn_revision)


    def nuget(self):
        cmd = 'nuget.exe restore'
        DemoDosser.exe(cmd)

        lib = os.path.join(self.name, 'lib')

        sql = '''
            WITH RECURSIVE r AS (
                SELECT %d AS package_id
                UNION
                SELECT dp.dependent_package_id AS package_id FROM r JOIN dependent_packages AS dp USING(package_id) WHERE r.package_id = dp.package_id
            )
            SELECT p.name FROM r JOIN packages AS p ON r.package_id = p.id WHERE p.id != %d;
        ''' % (self.package_id, self.package_id)
        package_rows = self.exe_sql(sql)

        for package_row in package_rows:
            package = package_row[0]

            # get the max version of package
            sql = '''SELECT MAX(version) FROM public."%s";''' % package
            max_version_rows = self.exe_sql(sql)
            if not max_version_rows:
                logging.error('Version of %s not found.' % package)
                exit(1)
            max_version = '.'.join(str(number) for number in max_version_rows[0][0])

            filename = '%s-%s' % (package, max_version)
            filename += '.zip'
            path_file = '%s/%s/%s' % (self.mini_releases, package, filename)
            if not DemoDosser.scp_test(path_file):
                logging.error('No such file: %s' % path_file)
                exit(1)

            DemoDosser.scp(path_file, lib)


    def run_before_build(self):
        self.package_id = None
        sql = '''SELECT id FROM public.packages WHERE name = '%s';''' % self.name
        package_id_rows = self.exe_sql(sql)
        if package_id_rows:
            self.package_id = package_id_rows[0][0]
        logging.info('package_id: %s' % self.package_id)

        (old_pg_version, old_git_revision, old_svn_revision) = self.get_pg_version()

        new_git_revision = self.get_git_revision()

        new_svn_revision = old_svn_revision
        if self.git_to_svn:
            if self.force or old_git_revision != new_git_revision:
                new_svn_revision = self.commit_git_to_svn(old_git_revision, old_svn_revision)
        
        new_pg_version = self.calc_new_pg_version(old_pg_version, old_git_revision, old_svn_revision, new_git_revision, new_svn_revision)

        new_pg_version_str = '.'.join([str(i) for i in new_pg_version])
        self.set_properties_assembly_info(new_pg_version_str)

        self.nuget()

        bin = os.path.join(self.name, 'bin')
        if os.path.exists(bin):
            shutil.rmtree(bin)

        return (new_pg_version_str, new_git_revision, new_svn_revision)


    def build(self, properties, msbuildpath=''):
        properties_str_list = []
        for key, value in properties.items():
            item = '-property:%s="%s"' % (key, value)
            properties_str_list.append(item)
        properties_str = ' '.join(properties_str_list)

        cmd = '%smsbuild.exe %s %s\%s.csproj'
        cmd = cmd % (msbuildpath, properties_str, self.name, self.name)
        DemoDosser.exe(cmd)


    def run_after_build(self, new_pg_version_str, new_git_revision, new_svn_revision):
        if self.pg_version is not None:
            return

        self.set_pg_version(new_pg_version_str, new_git_revision, new_svn_revision)


if __name__ == '__main__':
    logger = DemoLogger(file=False)

    get_opts_and_args(sys.argv[1:])

    logging.info('cd %s' % valid_opts['root_directory'])
    os.chdir(valid_opts['root_directory'])

    dba = DemoDataBaseAdministrator('postgresql')
    if not dba.connect(config, service):
        exit(1)

    version_controlller = DemoVersionController(
        valid_opts['name'],
        valid_opts['mini_releases'],
        valid_opts['start_index'],
        valid_opts['delta_index'],
        valid_opts['git_branch'],
        valid_opts['git_to_svn'],
        valid_opts['force'],
        valid_opts['svn_remote'],
        valid_opts['svn_username'],
        valid_opts['svn_password'],
        valid_opts['pg_version'],
    )

    version_controlller.connect_pg(dba.connection)
    version_controlller.run(valid_opts['properties'])
    version_controlller.disconnect_pg()
