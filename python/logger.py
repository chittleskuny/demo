#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os
import time


class DemoLogger(object):
    def __init__(self, name=None, format=None, stream=True, file=True):
        self.time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())

        self.format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
        if format is not None:
            self.format = format
        
        if not os.path.exists('logs'):
            os.makedirs('logs')

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        if stream:
            sh = logging.StreamHandler()
            sh.setFormatter(logging.Formatter(self.format))
            sh.setLevel(logging.DEBUG)
            logger.addHandler(sh)

        if file:
            filename = '%s.log' % self.time_str
            if name is not None:
                filename = '%s_%s' % (name, filename)
            path_file = os.path.join('logs', filename)
            fh = logging.FileHandler(path_file)
            fh.setFormatter(logging.Formatter(self.format))
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)


class DemoLoggerTree(object):
    def __init__(self, name=None, format=None, stream=True, file=True):
        self.time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())

        self.format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
        if format is not None:
            self.format = format

        if not os.path.exists('logs'):
            os.makedirs('logs')

        self._init_node('Lv0', '[0] %s' % self.format)
        self._init_node('Lv0.Lv1', '[1] %s' % self.format)
        self._init_node('Lv0.Lv1.Lv2', '[2] %s' % self.format)


    def _init_node(self, name, format=None, stream=True, file=True):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if stream:
            sh = logging.StreamHandler()
            sh.setFormatter(logging.Formatter(format))
            sh.setLevel(logging.DEBUG)
            logger.addHandler(sh)

        if file:
            filename = '%s_%s.log' % (name.replace('.', '_'), self.time_str)
            path_file = os.path.join('logs', filename)
            fh = logging.FileHandler(path_file)
            fh.setFormatter(logging.Formatter(format))
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)


if __name__ == '__main__':

    DemoLogger(name='myself')

    logging.debug('debug message.')
    logging.info('info message.')
    logging.warning('warning message.')
    logging.error('error message.')

    ######

    DemoLoggerTree()
    logging.debug('Start')

    logger = logging.getLogger()
    logger.debug('Root')

    logger_lv0 = logging.getLogger('Lv0')
    logger_lv0.debug('000')

    logger_lv1 = logging.getLogger('Lv0.Lv1')
    logger_lv1.debug('111')

    logger_lv2 = logging.getLogger('Lv0.Lv1.Lv2')
    logger_lv2.debug('222')
