# coding: utf-8
import os

import sqlite3

import datetime


class Repository:
    def __init__(self, root):
        self.root = root

        self.conn = sqlite3.connect(
            os.path.join(self.root, 'pxv.db'),
            detect_types=sqlite3.PARSE_DECLTYPES
        )

    def test(self):
        conn = self.conn

        with conn:
            cur = conn.execute(r'select * from image_content')

            for row in cur.fetchall():
                print(row)


if __name__ == '__main__':
    repo = Repository('..')

    repo.test()
