#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os
import time


class DemoLogger(object):
    def __init__(self, stream=True, file=True, target=None):
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())

        logger = logging.getLogger()
        format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
        logger.setLevel(logging.DEBUG)

        if stream:
            sh = logging.StreamHandler()
            sh.setFormatter(logging.Formatter(format))
            sh.setLevel(logging.DEBUG)
            logger.addHandler(sh)

        if file:
            if not os.path.exists('logs'):
                os.makedirs('logs')
            filename = '%s.log' % time_str
            if target is not None:
                filename = '%s_%s' % (target, filename)
            path_file = os.path.join('logs', filename)
            fh = logging.FileHandler(path_file)
            fh.setFormatter(logging.Formatter(format))
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)


class DemoLoggerTree(object):
    def __init__(self):
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())

        # Lv0
        name = 'Lv0' # root
        logger = logging.getLogger()
        format = '%(asctime)s %(levelname)s %(filename)s[%(lineno)d] [0] %(message)s'
        logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(format))
        sh.setLevel(logging.DEBUG)
        logger.addHandler(sh)

        fh = logging.FileHandler('%s.log' % time_str)
        fh.setFormatter(logging.Formatter(format))
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

        # Lv1
        name = 'Lv1'
        logger = logging.getLogger(name)
        format = '%(asctime)s %(levelname)s %(filename)s[%(lineno)d] [1] %(message)s'
        logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(format))
        sh.setLevel(logging.DEBUG)
        logger.addHandler(sh)

        fh = logging.FileHandler('%s_%s.log' % (time_str, name.replace('.', '_')))
        fh.setFormatter(logging.Formatter(format))
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

        # Lv2
        name = 'Lv1.Lv2'
        logger = logging.getLogger(name)
        format = '%(asctime)s %(levelname)s %(filename)s[%(lineno)d] [2] %(message)s'
        logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(format))
        sh.setLevel(logging.DEBUG)
        logger.addHandler(sh)

        fh = logging.FileHandler('%s_%s.log' % (time_str, name.replace('.', '_')))
        fh.setFormatter(logging.Formatter(format))
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)


if __name__ == '__main__':
    DemoLogger(target='myself')

    logging.debug('debug message.')
    logging.info('info message.')
    logging.warning('warning message.')
    logging.error('error message.')
