#!/usr/bin/python
# -*- coding:utf-8 -*-

import getopt
import html
import os
import shutil
import sys
import urllib.parse

from database_administrator import *
from logger import *

valid_opts = {
    'config': None,
    'service': None,
    'root': '.',
    'force': False,
}
valid_args = []

def get_opts_and_args(argv):
    try:
        opts, args = getopt.getopt(argv, '', [
            'help',
            'config=',
            'service=',
            'root=',
            'force',
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
        elif opt in ('--root'):
            valid_opts['root'] = arg
        elif opt in ('--force'):
            valid_opts['force'] = True
        else:
            logging.warning('unknown opt: %s.' % opt)
    
    logging.info('config: %s' % valid_opts['config'])
    logging.info('service: %s' % valid_opts['service'])
    logging.info('root: %s' % valid_opts['root'])
    logging.info('force: %s' % valid_opts['force'])

    valid_args = args
    logging.info('valid_args: %s' % valid_args)


class DemoWordPressEditor(object):
    def __init__(self, dba, root, force=False):
        self.dba = dba
        self.root = root
        self.pull(force)


    def pull(self, force=False):
        root_posts = os.path.join(self.root, 'posts')
        if os.path.exists(root_posts):
            if force:
                logging.warning('Remove dir %s' % root_posts)
                shutil.rmtree(root_posts)
            else:
                return

        os.makedirs(root_posts)
        self._pull_categories(root_posts)


    def _pull_categories(self, root_posts):
        cursor = self.dba.open_cursor()
        sql = '''
            SELECT
                term_id,
                name,
                slug
            FROM
                wp_term_taxonomy JOIN wp_terms USING(term_id)
            WHERE taxonomy = 'category';
        '''
        dba.execute(cursor, sql)
        category_rows = dba.fetchall(cursor)
        cursor.close()

        for category_row in category_rows:
            (
                term_id,
                name,
                slug,
            ) = category_row
            root_posts_category = os.path.join(root_posts, name)
            logging.info('Pull %s' % root_posts_category)
            os.mkdir(root_posts_category)

            root_posts_category_readme = os.path.join(root_posts, name, 'readme.md')
            with open(root_posts_category_readme, 'w', encoding='utf-8', newline='\n') as f:
                content = '''
                    ---
                    term_id: %d
                    slug: %s
                    ---
                '''.replace('    ', '') % (
                    term_id,
                    urllib.parse.unquote(slug),
                )
                f.write(content)

            self._pull_category_posts(root_posts_category, term_id)


    def _pull_category_posts(self, root_posts_category, term_id):
        cursor = self.dba.open_cursor()

        sql = '''
            SELECT
                d.ID,
                d.post_date,
                d.post_title,
                d.post_content_filtered
            FROM
                wp_terms AS a
                JOIN wp_term_taxonomy AS b ON b.term_id = a.term_id
                JOIN wp_term_relationships AS c ON c.term_taxonomy_id = b.term_taxonomy_id
                JOIN wp_posts AS d ON d.ID = c.object_id
            WHERE
                a.term_id = %d
                AND d.post_type IN ('post', 'page');
        ''' % term_id
        dba.execute(cursor, sql)
        post_rows = dba.fetchall(cursor)
        cursor.close()

        for post_row in post_rows:
            (
                ID,
                post_date,
                post_title,
                post_content_filtered,
            ) = post_row

            post = '''[%s] [p%d] %s.md''' % (
                time.strftime('%Y%m%d_%H%M%S', post_date.timetuple()),
                ID,
                post_title,
            )
            root_posts_post = os.path.join(root_posts_category, post)
            logging.info('Pull %s' % root_posts_post)
            
            with open(root_posts_post, 'w', encoding='utf-8', newline='\n') as f:
                content = html.unescape(post_content_filtered).replace('\r\n', '\n')
                f.write(content)


    def push(self):
        pass


if __name__ == '__main__':
    DemoLogger(file_enable=False)

    get_opts_and_args(sys.argv[1:])

    dba = DemoDataBaseAdministrator('mysql')
    if dba.connect(valid_opts['config'], valid_opts['service']):
        wpe = DemoWordPressEditor(dba, valid_opts['root'], valid_opts['force'])
        dba.disconnect()
