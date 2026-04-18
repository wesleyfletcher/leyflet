import mysql.connector as sql
import pandas as pd

import os
from dotenv import load_dotenv

class database:
    global cursor
    global schema

    def __init__(self):
        load_dotenv()

        self.schema = sql.connect(
            host=os.getenv('MYSQLHOST'),
            port=int(os.getenv('MYSQLPORT')),
            user=os.getenv('MYSQLUSER'),
            password=os.getenv('MYSQLPASSWORD'),
            database=os.getenv('MYSQLDATABASE')
        )
        self.cursor = self.schema.cursor()

    def close(self):
        self.schema.disconnect()

    def commit(self):
        self.schema.commit()

    def query(self, qry : str, rows=-1) -> pd.DataFrame:
        if rows > -1:
            qry += f' LIMIT {rows}'

        self.cursor.execute(qry)

        df = pd.DataFrame(columns=self.cursor.column_names)
        for x in self.cursor:
            df.loc[len(df)] = x

        df = df.replace({float('nan'): None})

        if len(df) == 1 and len(df.columns) == 1:
            return df.iloc[0, 0]
        
        return df
    
    def runfile(self, file : str, **kwargs):
        sql_file = open(f'static/sql/{file}.sql', 'r')

        qry = sql_file.read().replace('\n', ' ')

        blocks = qry.split()
        for blk in blocks:
            if '{' in blk:
                start = blk.index('{')
                end = blk.index('}')

                qry = qry.replace(blk[start:end+1], str(kwargs[blk[start+1:end]]))

        sql_file.close()

        return self.query(qry)
    
    def execute(self, qry : str):
        self.cursor.execute(qry)

    def show(self, tbl : str, rows=-1) -> pd.DataFrame:
        qry = f'SELECT * FROM {tbl}'
        return self.query(qry, rows)

    def describe(self, tbl : str, rows=-1) -> pd.DataFrame:
        qry = f'DESCRIBE {tbl}'
        return self.query(qry, rows=rows)

    def insert(self, tbl : str, vals, cols=None):
        # Single row
        if type(vals[0]) not in [list, set, tuple, pd.Series]:
            size = len(vals)
            single = True

        # Multiple rows
        else:
            size = len(vals[0])
            single = False

        format = size*'%s, '
        format = format[:-2]

        if cols is None:
            qry = f'INSERT INTO {tbl} VALUES ({format})'
        else:
            col_str = ''
            for col in cols:
                col_str += col + ', '
            col_str = col_str[:-2]

            qry = f'INSERT INTO {tbl}({col_str}) VALUES ({format})'

        if single:
            self.cursor.execute(qry, vals)
        else:
            self.cursor.executemany(qry, vals)