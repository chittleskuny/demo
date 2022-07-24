#!/usr/bin/python
# -*- coding:utf-8 -*-

import configparser
import logging
import os
import sys


class DemoDataBaseAdministrator(object):
    def __init__(self, brand):
        self.brand = brand.lower()
        self.connection = None


    def connect(self, config, service):
        cp = configparser.ConfigParser()

        if not os.path.isfile(config):
            return False

        cp.read(config)
        if service not in cp:
            return False

        if not hasattr(self, 'connect_' + self.brand):
            return False

        function = getattr(self, 'connect_' + self.brand)
        self.connection = function(cp[service])
        if not self.connection:
            print('Failure.')
            return False

        print('Success.')
        return True


    def connect_sqlite(self, items):
        import sqlite3

        if 'database' not in items:
            return None
        else:
            database = items['database']

        return sqlite3.connect(database)


    def connect_mysql(self, items):
        # pip install mysql-connector
        import mysql.connector
        
        host = 'localhost'
        if 'host' in items:
            host = items['host']

        port = 3306
        if 'port' in items:
            port = items['port']

        user = 'root'
        if 'user' in items:
            user = items['user']
        
        if 'password' not in items:
            return None
        else:
            password = items['password']
        
        if 'database' not in items:
            return None
        else:
            database = items['database']

        return mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            auth_plugin='mysql_native_password'
        )


    def connect_postgresql(self, items):
        import psycopg2

        host = 'localhost'
        if 'host' in items:
            host = items['host']

        port = 5432
        if 'port' in items:
            port = items['port']

        user = 'root'
        if 'user' in items:
            user = items['user']
        
        if 'password' not in items:
            return None
        else:
            password = items['password']
        
        if 'database' not in items:
            return None
        else:
            database = items['database']

        return psycopg2.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = database,
        )


    def disconnect(self):
        return self.connection.close()


    def open_cursor(self):
        return self.connection.cursor()


    def close_cursor(self, cursor):
        return cursor.close()


    def execute(self, cursor, sql):
        sql = sql.replace('    ', '')
        logging.info(sql)
        return cursor.execute()


    def fetchall(self, cursor):
        return cursor.fetchall()


    def fetchone(self, cursor):
        return cursor.fetchone()


    def commit(self):
        return self.connection.commit()


    def get_table_names(self, cursor, table_schema):
        if self.brand == 'sqlite':
            rows = None
        elif self.brand == 'mysql':
            sql = '''
                'SELECT table_name FROM information_schema.tables WHERE table_schema=\'%s\';'
            ''' % table_schema
            cursor.execute(sql)
            rows = cursor.fetchall()
        elif self.brand == 'postgresql':
            sql = '''
                SELECT table_name FROM pg_tables;
            '''
            cursor.execute(sql)
            rows = cursor.fetchall()
        else:
            rows = None

        return rows


    def get_create_table(self, table_schema, table_name):
        return None


    def get_table_columns(self, table_schema, table_name):
        return None


if __name__ == '__main__':
    if len(sys.argv) <= 3:
        exit(1)
    
    brand = sys.argv[1]
    config = sys.argv[2]
    service = sys.argv[3]

    dba = DemoDataBaseAdministrator(brand)

    if not dba.connect(config, service):
        exit(1)

    cursor = dba.open_cursor()
    dba.execute(cursor, 'SHOW TABLES;')
    print(dba.fetchall(cursor))
    
    dba.disconnect()
