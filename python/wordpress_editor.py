#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

from database_administrator import *
from logger import *


class DemoWordPressEditor(object):
    def __init__(self, dba, root):
        self.dba = dba
        self.root = root
        self.pull()


    def pull(self):
        root_posts = os.path.join(root, 'posts')
        logging.debug(root_posts)
        if os.path.exists(root_posts):
            return

        os.mkdir(root_posts)
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
                    slug,
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

            post = '''[%s] %s.md''' % (
                time.strftime('%Y%m%d_%H%M%S', post_date.timetuple()),
                post_title,
            )
            root_posts_post = os.path.join(root_posts_category, post)
            logging.info('Pull %s' % root_posts_post)
            
            with open(root_posts_post, 'w', encoding='utf-8', newline='\n') as f:
                content = '''
                    ---
                    ID: %d
                    ---

                    %s
                '''.replace('    ', '') % (
                    ID,
                    post_content_filtered.replace('\r\n', '\n'),
                )
                f.write(content)


    def push(self):
        pass


if __name__ == '__main__':
    DemoLogger(file=False)

    if len(sys.argv) <= 3:
        exit(1)

    root = sys.argv[1]
    config = sys.argv[2]
    service = sys.argv[3]

    dba = DemoDataBaseAdministrator('mysql')
    if dba.connect(config, service):
        wpe = DemoWordPressEditor(dba, root)
        dba.disconnect()
