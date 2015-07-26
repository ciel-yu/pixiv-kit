# coding: utf-8


import sqlite3

with sqlite3.connect('pxv.db') as conn:

    c = conn.execute('select * from sqlite_master')

    print(c.fetchall())
