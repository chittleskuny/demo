#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import string
import sys


class Passer:
    def __init__(self):
        pass
    
    
    def getChars(self):
        ascii_letters = list(string.ascii_letters)
        for char in 'CcIiLlOoPpSsUuVvWwXxZz':
            ascii_letters.remove(char)
        ascii_letters = ''.join(ascii_letters)

        digits = list(string.digits)
        for char in '01':
            digits.remove(char)
        digits = ''.join(digits)

        return ascii_letters + digits


    def generate(self, length):
        return ''.join(random.sample(self.getChars(), length))


if __name__ == '__main__':
    if len(sys.argv) < 1:
        exit(1)
    
    print(Passer().generate(int(sys.argv[1])))
