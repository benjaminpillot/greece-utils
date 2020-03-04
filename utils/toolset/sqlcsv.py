# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'

import csv

from sqlalchemy import MetaData, Table
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import sessionmaker


class SqlCsv:
    """

    """

    def __init__(self, engine, session):
        """ Build SqlCsv class instance

        :param engine: sqlalchemy engine
        :param session: corresponding sqlalchemy session
        """
        self.engine = engine
        self.session = session
        self.inspector = Inspector.from_engine(self.engine)
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)

    def to_csv(self, table_name, csv_file, get_foreign_key_tables=False, delimiter=','):
        """ Convert sql database table to csv

        :param table_name: table name in sqlalchemy ORM
        :param csv_file: path to csv file
        :param get_foreign_key_tables: if True, try to map all corresponding tables (from foreign keys) into csv
        :param delimiter: delimiter char in csv file (default: comma)
        :return:
        """
        def get_columns(name, no_id=False):
            """ Recursively get all column names from all tables in database

            :param name: table name
            :param no_id: only used for recursive calls (no more id column for related tables)
            :return:
            """
            if no_id:
                columns = [column.name for column in self.meta.tables[name].c if column.name != "id"]
            else:
                columns = [column.name for column in self.meta.tables[name].c]

            foreign_keys = self.inspector.get_foreign_keys(name)
            if foreign_keys:
                for foreign_key in foreign_keys:
                    referred_table = foreign_key['referred_table']
                    columns.extend(get_columns(referred_table, no_id=True))

            return columns

        def get_row_from_id(name, _id, no_id=False):
            """ Recursively get all rows from all tables in database

            :param name: table name
            :param _id:
            :param no_id:
            :return:
            """
            query = self.session.query(self.meta.tables[name]).filter(self.meta.tables[name].c.id == _id).one()
            if no_id:
                row_ = [query.__getattribute__(column.name) for column in self.meta.tables[name].c
                        if column.name != "id"]
            else:
                row_ = [query.__getattribute__(column.name) for column in self.meta.tables[name].c]

            foreign_keys = self.inspector.get_foreign_keys(name)
            if foreign_keys:
                for foreign_key in foreign_keys:
                    ref_id = query.__getattribute__(foreign_key['constrained_columns'][0])
                    row_.extend(get_row_from_id(foreign_key['referred_table'], ref_id, no_id=True))

            return row_

        results = self.session.query(self.meta.tables[table_name]).all()

        if get_foreign_key_tables:
            rows = []
            column_names = get_columns(table_name)
            for result in results:
                rows.append(get_row_from_id(table_name, result.id))

        else:
            column_names = [column.name for column in self.meta.tables[table_name].c]
            rows = [[result.__getattribute__(name) for name in column_names] for result in results]

        with open(csv_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=delimiter)
            csvwriter.writerow(column_names)
            for row in rows:
                csvwriter.writerow(row)
