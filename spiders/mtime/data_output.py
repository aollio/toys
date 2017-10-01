#!/usr/bin/env python3

import sqlite3
import os

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class DataOutput:
    def __init__(self):
        if not os.path.exists('dist'):
            os.mkdir('dist')
        self.cx = sqlite3.connect(os.path.join('dist', 'mtime.db'))
        self.create_table('mtime')
        self.data = []

    def create_table(self, table_name):

        value = '''
        id integer primary key,
        movie_id integer not null,
        movie_title varchar(40) not null,
        rating_final real not null default 0.0,
        rother_final real not null default 0.0,
        rpicture_final real not null default 0.0,
        rdirector_final real not null default 0.0,
        rstory_final real not null default 0.0,
        user_count integer not null default 0,
        attitude_count integer not null default 0,
        total_box_office varchar(20) not null,
        today_box_office varchar(20) not null,
        rank integer not null default 0,
        show_days integer not null default 0,
        is_release integer not null
        '''
        self.cx.execute('create table if not exists %s (%s)' % (table_name, value))

    def store_data(self, data):
        """

        :param data:
        :return:
        """
        if data is None:
            return

        self.data.append(data)
        if len(self.data) > 10:
            self.output_db('mtime')

    def output_db(self, table_name):
        """
        将数据存储到sqlite3
        :param table_name:
        :return:
        """
        for item in self.data:
            self.cx.execute('INSERT INTO %s (movie_id, movie_title,'
                            'rating_final, rother_final, rpicture_final,'
                            'rdirector_final, rstory_final, user_count,'
                            'attitude_count, total_box_office, today_box_office,'
                            'rank, show_days, is_release) VALUES '
                            '(?,?,?,?,?,?,?,?,?,?,?,?,?,?)' % table_name, item)
            self.data.remove(item)

        self.cx.commit()

    def output_end(self):

        if len(self.data) > 0:
            self.output_db('mtime')
        self.cx.close()
