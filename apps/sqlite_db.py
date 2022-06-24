# -*- coding: utf-8 -*-
import sqlite3 as sql
from sqlite3 import Error


class DBM(object):
    """ Database Manager (DBM) class and DBM(object) functions """
    def __init__(self, db):
        """ create a database connection to a SQLite database """
        self.conn = sql.connect(db, check_same_thread=False)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def __del__(self):
        """ close connection """
        self.conn.close()

    def attach(self, db_file, ref_name):
        """ attach another database to the current connection """
        self.cur.execute('ATTACH DATABASE '+str(db_file)+' AS '+str(db_name))
        self.conn.commit()

    def create_table(self, create_table_sql):
        """ create a table from the sql statement """
        try:
            self.cur.execute(create_table_sql)
        except Error as e:
            print(e)

    def delete_table(self, table_name):
        """ create a table from the sql statement """
        try:
            self.cur.execute("DROP table IF EXISTS "+str(table_name))
        except Error as e:
            print(e)

    def insert_entry(self, insert_entry_sql, entry_value):
        """ insert a new entrty into the sql table """
        self.cur.execute(insert_entry_sql, entry_value)
        self.conn.commit()
        return self.cur.lastrowid

    def update_entry(self, update_entry_sql, entry):
        """update fields of an entry """
        self.cur.execute(update_entry_sql, entry)
        self.conn.commit()

    def delete_entry(self, table_name, query_field, value):
        """ delete an entry by query_field value """
        sql = "DELETE FROM "+str(table_name)
        if query_field != '':
            sql += " WHERE "+str(query_field)+"=?"
            self.cur.execute(sql, (value,))
        else:
            self.cur.execute(sql)
        self.conn.commit()

    def query(self, table_name, select_field, query_field, value):
        """ select data from sql table by querying a given field  """
        if select_field == '':
            select_field = '*'
        sql = "SELECT "+select_field+" FROM "+str(table_name)
        if query_field != '':
            sql += " WHERE "+str(query_field)+"=?"
            self.cur.execute(sql, (value,))
        else:
            self.cur.execute(sql)
        self.conn.commit()
        rows = self.cur.fetchall()
        return rows


##---- SQL STATEMENTS ----##

create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                            id integer PRIMARY KEY,
                            name text NOT NULL,
                            location text,
                            tabs text
                        ); """


create_tabs_table = """ CREATE TABLE IF NOT EXISTS tabs (
                            id integer PRIMARY KEY,
                            tab_id text NOT NULL,
                            name text NOT NULL,
                            status_id integer NOT NULL,
                            project_id integer NOT NULL,
                            pipeline text NOT NULL,
                            charts text NOT NULL,
                            FOREIGN KEY (project_id) REFERENCES projects (id)
                        ); """


insert_project = ''' INSERT INTO projects(name,location,tabs)
                    VALUES(?,?,?) '''


insert_tab = ''' INSERT INTO tabs(tab_id,name,status_id,project_id,pipeline,charts)
                 VALUES(?,?,?,?,?,?) '''


update_project = ''' UPDATE tasks
                     SET name = ? ,
                         location = ? ,
                         tabs = ?
                     WHERE id = ?'''


update_tab = ''' UPDATE tasks
                 SET tab_id = ? ,
                     name = ? ,
                     status_id = ? ,
                     project_id = ?,
                     pipeline = ?,
                     charts = ?
                 WHERE id = ?'''

