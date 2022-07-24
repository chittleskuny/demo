#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

from .database_administrator import *
from .logger import *


class DemoWordPressEditor(object):
    def __init__(self, dba, root):
        self.dba = dba
        self.root = root

        self.pull()

        
    def pull(self):
        root_posts = os.path.join(root, 'posts')
        if os.path.exists(root_posts):
            return

        os.mkdir(root_posts)
        cursor = self.dba.open_cursor()
        dba.execute(cursor, 'SHOW TABLES;')
        rows = dba.fetchall(cursor)
        print(rows)


    def push(self):
        pass


if __name__ == '__main__':
    if len(sys.argv) <= 3:
        exit(1)

    root = sys.argv[1]
    config = sys.argv[2]
    service = sys.argv[3]

    dba = DemoDataBaseAdministrator('mysql')
    if dba.connect(config, service):
        wpe = DemoWordPressEditor(dba, root)
        dba.disconnect()
