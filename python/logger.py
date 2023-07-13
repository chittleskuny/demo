#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import time


class DemoLogger(object):
    def __init__(
            self,
            filename = None,
            pathname='logs',
            format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s',
            stream_enable = True,
            file_enable = True
        ):
        self.time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())

        self.filename = filename
        self.pathname = pathname

        self.format = format
        
        if not os.path.exists(self.pathname):
            os.makedirs(self.pathname)

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        if stream_enable:
            sh = logging.StreamHandler()
            sh.setFormatter(logging.Formatter(self.format))
            sh.setLevel(logging.DEBUG)
            logger.addHandler(sh)

        if file_enable:
            full_filename = '%s.log' % self.time_str
            if self.filename is not None:
                full_filename = '%s_%s' % (self.filename, full_filename)
            path_file = os.path.join(self.pathname, full_filename)
            fh = logging.FileHandler(path_file)
            fh.setFormatter(logging.Formatter(self.format))
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            logging.info(full_filename)


class DemoLoggerTree(object):
    def __init__(
            self,
            filename = None,
            pathname='logs',
            format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s',
            stream_enable = True,
            file_enable = True
        ):
        self.time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())

        self.filename = filename
        self.pathname = pathname

        self.format = format

        if not os.path.exists(self.pathname):
            os.makedirs(self.pathname)

        self._init_node('Lv0', '[0] %s' % self.format)
        self._init_node('Lv0.Lv1', '[1] %s' % self.format)
        self._init_node('Lv0.Lv1.Lv2', '[2] %s' % self.format)


    def _init_node(self, node, format = None, stream_enable = True, file_enable = True):
        logger = logging.getLogger(node)
        logger.setLevel(logging.DEBUG)

        if stream_enable:
            sh = logging.StreamHandler()
            sh.setFormatter(logging.Formatter(format))
            sh.setLevel(logging.DEBUG)
            logger.addHandler(sh)

        if file_enable:
            full_filename = '%s_%s.log' % (node, self.time_str)
            if self.filename is not None:
                full_filename = '%s_%s' % (self.filename.replace('.', '_'), full_filename)
            path_file = os.path.join(self.pathname, full_filename)
            fh = logging.FileHandler(path_file)
            fh.setFormatter(logging.Formatter(format))
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)


if __name__ == '__main__':

    # DemoLogger

    DemoLogger()

    logging.debug('debug message.')
    logging.info('info message.')
    logging.warning('warning message.')
    logging.error('error message.')

    # DemoLoggerTree

    DemoLoggerTree(filename='tree')
    logging.debug('Start')

    logger = logging.getLogger()
    logger.debug('Root')

    logger_lv0 = logging.getLogger('Lv0')
    logger_lv0.debug('000')

    logger_lv1 = logging.getLogger('Lv0.Lv1')
    logger_lv1.debug('111')

    logger_lv2 = logging.getLogger('Lv0.Lv1.Lv2')
    logger_lv2.debug('222')
