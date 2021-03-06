import sqlite3
import os

class DBUtil:

    def __init__(self, app, test):
        self.app = app
        self.test = test
        if test:
            self.init_test_db()
            self.connect_db = self.connect_test_db
        else:
            self.init_db()
            self.connect_db = self.connect_real_db
 
    def connect_real_db(self):
        rv = sqlite3.connect(self.app.config['DATABASE']) 
        rv.row_factory = create_dictionary
        return rv

    def init_db(self):
        if os.path.isfile(self.app.config['DATABASE']):
            os.remove(self.app.config['DATABASE'])

        rv = sqlite3.connect(self.app.config['DATABASE'])
        rv.row_factory = create_dictionary
        with self.app.open_resource('shopstop.sql', mode='r') as f:
            rv.cursor().executescript(f.read())
        rv.commit()
        return rv

    def init_test_db(self):
        if os.path.isfile('./testdb.db'):
            os.remove('testdb.db')

        rv = sqlite3.connect('testdb.db')
        rv.row_factory = create_dictionary
        with self.app.open_resource('shopstop.sql', mode='r') as f:
            rv.cursor().executescript(f.read())
        rv.commit()
        return rv
    
    def connect_test_db(self):
        rv = sqlite3.connect('testdb.db')
        rv.row_factory = create_dictionary
        return rv

    def multiple_return_query(self, query, params):
        rv = self.connect_db()
        cursor = rv.cursor()
        cursor.execute(query, params)
        values = cursor.fetchall()
        rv.close()
        return values
    
    def single_return_query(self, query, params):
        rv = self.connect_db()
        cursor = rv.cursor()
        cursor.execute(query, params)
        value = cursor.fetchone()
        rv.close()
        return value

    def no_return_query(self, query, params, commit):
        rv = self.connect_db()
        cursor = rv.cursor()
        cursor.execute(query, params)

        if commit:
            rv.commit()
            rv.close()
        else:
            return rv

    def multiple_no_return_query(self, queries, params):
        rv = self.connect_db()
        cursor = rv.cursor()
        for i in range(0, len(queries)):
            cursor.execute(queries[i], params[i])
        rv.commit()
        rv.close()


def create_dictionary(cursor, row):
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result