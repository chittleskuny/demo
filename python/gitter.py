#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import git
import os
import sys

from colorama import init, Fore


expected_repo_location_user_name = {
    'github': 'Chittle Skuny',
}

expected_repo_location_user_email = {
    'github': 'chittleskuny@gmail.com',
}


class DemoGitter():
    def __init__(self, folders_txt):
        self.folders = []
        self.get_folders(folders_txt)

        self.repos = []
        if self.folders:
            self.get_repos()


    def get_folders(self, folders_txt):
        with open(folders_txt) as f:
            lines = f.readlines()
            for line in lines:
                folder = line.strip()
                self.folders.append(folder)


    def get_repos(self):
        for folder in self.folders:
            for root, dirs, files in os.walk(folder):
                for dir in dirs:
                    
                    root_dir = os.path.join(root, dir)
                    if root_dir.find('.git') != -1:
                        continue

                    root_dir_git = os.path.join(root_dir, '.git')
                    if os.path.exists(root_dir_git):
                        self.repos.append(root_dir)

        self.repos.sort()


    def get_status(self):
        for repo in self.repos:
            print('')
            git_repo = git.Repo(repo)

            repo_path_split = os.path.split(repo)
            repo_path_list = repo_path_split[0].split('\\')
            repo_location = repo_path_list[2]
            repo_name = '/'.join(repo_path_list[3:] + [repo_path_split[1]])
            
            if str(git_repo.active_branch) == 'master':
                print('[%s] %s (%s)' % (repo_location, repo_name, git_repo.active_branch))
            else:
                print('[%s] %s %s(%s)' % (repo_location, repo_name, Fore.YELLOW, git_repo.active_branch))

            stash_list = git_repo.git.stash('list')
            if stash_list:
                print('%s%s' % (Fore.YELLOW, stash_list))

            user_name = None
            user_email = None

            for lit_config_level in ['global', 'system', 'repository']:
                git_config_parser = git_repo.config_reader(lit_config_level)
                try:
                    user_name = git_config_parser.get('user', 'name')
                    user_email = git_config_parser.get('user', 'email')
                except configparser.NoSectionError:
                    pass
                except configparser.NoOptionError:
                    pass
                except KeyError:
                    pass

            if (repo_location in expected_repo_location_user_name and expected_repo_location_user_name[repo_location] != user_name) or \
                    (repo_location in expected_repo_location_user_email and expected_repo_location_user_email[repo_location] != user_email):
                print('%s%s<%s>' % (Fore.RED, user_name, user_email))
            else:
                print('%s<%s>' % (user_name, user_email))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        exit(1)
    
    folders = sys.argv[1]

    init(autoreset = True)
    
    gitter = DemoGitter(folders)
    gitter.get_status()
