#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class DemoCat():
    def __init__(self, prt_flag = False):
        self.blk_size = 1024
        self.prt_flag = prt_flag

    def _more(self, path_file, num = 1000):
        return []

    def _less(self, path_file, num = 1000):
        return []

    def _head(self, path_file, num = 1000):
        return []

    def _tail(self, path_file, num = 1000):
        tails = []
        with open(path_file, 'rb') as fp:
            fp.seek(0, os.SEEK_END)
            cur_pos = fp.tell()
            while cur_pos > 0 and len(tails) < num:
                blk_size = min(self.blk_size, cur_pos)
                fp.seek(cur_pos - blk_size, os.SEEK_SET)
                blk_data = fp.read(blk_size)
                assert len(blk_data) == blk_size
                lines = blk_data.split(b'\n')

                # adjust cur_pos
                cur_tails = []
                if len(lines) > 1 and len(lines[0]) > 0:
                    for line in lines[1:]:
                        cur_tails.append(line.decode('utf-8') + '\n')
                    cur_pos -= (blk_size - len(lines[0]))
                else:
                    for line in lines:
                        cur_tails.append(line.decode('utf-8') + '\n')
                    cur_pos -= blk_size
                tails[0:0] = cur_tails
                fp.seek(cur_pos, os.SEEK_SET)

        if len(tails) > 0 and len(tails[-1]) == 0:
            del tails[-1]

        if self.prt_flag:
            print(''.join(tails[-num:]))

        return tails[-num:]
