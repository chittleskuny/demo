#!/usr/bin/python
# -*- coding:utf-8 -*-


from django.forms import PasswordInput


class DemoDataBaseAdministrator(object):
    def __init__(self, brand):
        self.brand = brand.lower()
        self.connection = None


    def connect(self, host='localhost', port=None, user='yourusername', password='yourpassword', database='databasename'):
        if self.brand == 'sqlite':
            import sqlite3
            self.connection = sqlite3.connect(database)
        elif self.brand == 'mysql':
            import mysql.connector # pip install mysql-connector
            if port is None:
                port = 3306
            self.connection = mysql.connector.connect(host=host, port=port, user=user, passwd=password, auth_plugin='mysql_native_password')
            print(self.connection)
        else:
            self.connection = None

        if self.connection:
            print('Success.')
            return True
        else:
            print('Failure.')
            return False

    def disconnect(self):
        return self.connection.close()


    def open_cursor(self):
        return self.connection.cursor()


    def close_cursor(self, cursor):
        return cursor.close()


    def execute(self, cursor, sql):
        return cursor.execute(sql)


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
            cursor.execute('SELECT table_name FROM information_schema.tables WHERE table_schema=\'' + table_schema + '\';')
            rows = cursor.fetchall()
        else:
            rows = None

        return rows


    def get_create_table(self, table_schema, table_name):
        return None


    def get_table_columns(self, table_schema, table_name):
        return None


if __name__ == '__main__':
    dba = DemoDataBaseAdministrator('mysql')
    if dba.connect(user='root', password='******', database='world'):
        cursor =dba.open_cursor()
        dba.execute(cursor, 'SHOW TABLES;')
        dba.disconnect()
