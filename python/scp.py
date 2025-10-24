#!/usr/bin/python
# -*- coding: utf-8 -*-


from logger import *


class DemoScp:
    def __init__(self, host, port, user):
        self.host = host
        self.port = port
        self.user = user

    def execute(self):
        pass

if __name__ == '__main__':
    if len(sys.argv) < 1:
        exit(1)

    print(DemoScp().generate(int(sys.argv[1])))