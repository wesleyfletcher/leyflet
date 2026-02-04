import mysql.connector as sql
import pandas as pd

class database:
    global cursor
    global schema

    def __init__(self):
        self.schema = sql.connect(
            host='localhost',
            user='root',
            password='Fletchdog04!', #make more secure
            database='leyflet'
        )
        self.cursor = self.schema.cursor()

    def close(self):
        self.schema.disconnect()

    def commit(self):
        self.schema.commit()

    def query(self, qry : str, rows=-1) -> pd.DataFrame:
        self.cursor.execute(qry)

        df = pd.DataFrame(columns=self.cursor.column_names)
        for x in self.cursor:
            df.loc[len(df)] = x

        if rows >= 0:
            df = df.head(rows)
        
        return df
    
    def execute(self, qry : str):
        self.cursor.execute(qry)

    def show(self, tbl : str, rows=-1) -> pd.DataFrame:
        qry = f'SELECT * FROM {tbl}'
        return self.query(qry, rows=rows)

    def describe(self, tbl : str, rows=-1) -> pd.DataFrame:
        qry = f'DESCRIBE {tbl}'
        return self.query(qry, rows=rows)

    def insert(self, tbl : str, vals):
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

        qry = f'INSERT INTO {tbl} VALUES ({format})'

        if single:
            self.cursor.execute(qry, vals)
        else:
            self.cursor.executemany(qry, vals)