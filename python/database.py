#!/usr/bin/python
# -*- coding:utf-8 -*-


# Demo Relational Data Base
class DemoRDB(object):
    def __init__(self, brand):
        self.brand = brand.lower()

    def connect_server(self, host='localhost', user='yourusername', passwd='yourpassword'):
        if self.brand == 'mysql':
            import mysql.connector
            conncection = mysql.connector.connect(host=host, user=user, passwd=passwd)
        else:
            conncection = None

        return conncection

    def connect_database(self, database='databasename'):
        if self.brand == 'sqlite':
            import sqlite3
            conncection = sqlite3.connect(database)
        else:
            conncection = None

        return conncection

    def disconnect(self, connection):
        return connection.close()

    def open_cursor(self, connection):
        return connection.cursor()

    def close_cursor(self, cursor):
        return cursor.close()

    def execute(self, cursor, sql):
        return cursor.execute(sql)

    def fetchall(self, cursor):
        return cursor.fetchall()

    def fetchone(self, cursor):
        return cursor.fetchone()

    def commit(self, connection):
        return connection.commit()

    def get_table_names(self, cursor, table_schema):
        if self.brand == 'mysql':
            cursor.execute('SELECT table_name FROM information_schema.tables WHERE table_schema=\'' + table_schema + '\';')
            rows = cursor.fetchall()
        return rows

    def get_create_table(self, table_schema, table_name):
        return None

    def get_table_columns(self, table_schema, table_name):
        return None


# Demo Non Relational Data Base
class DemoNRDB():
    def __init__(self, brand):
        self.brand = brand
