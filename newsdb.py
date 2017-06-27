#!/usr/bin/env python newsdb.py
# "Database code" for interfacing with the DB News.

import psycopg2


class PythonDatabaseInterface:
    """The class contains methods of connecting, """
    """closing a database and processing a query."""
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = psycopg2.connect(db_name)
        try:
            self.cursor = self.conn.cursor()
            print('Hello! Welcom to news!')
        except:
            print('Failed to connect news!')

    def print_helper(self, rows):
        for row in rows:
            print('    '+row[0]+' - '+str(row[1]) + ' views')
        print('----------------------------------------------------------------------')
        
    def get_data(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.print_helper(rows)

    def get_data_probability(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            print('    '+str(row[0])+' - '+str(row[1]) + '% errors')
        print('----------------------------------------------------------------------')
        
    def database_close(self):
        self.cursor.close()
        self.conn.close()

# Extract the string from log.path to match articles.slug
formatted_path = "(regexp_split_to_array(subsq.path, E'/article/'))[2]"

q1 = subsq+"select public.articles.title, nums from public.articles "\
     "join subsq on public.articles.slug = " + formatted_path +\
     "order by nums desc limit 3;"

q2 = viewer+"select public.authors.name, viewer.nums from public.authors, "\
     "viewer where public.authors.id = viewer.author "\
     "order by viewer.nums desc;"

# Only show the row(s) whose percentage is more than 1 %
q3 = view_total + view_error + view_final + \
     "select time, prob from final where prob > 1"

pdi = PythonDatabaseInterface("dbname=news")
print('Most popular articles:')
r1 = pdi.get_data(q1)
print('Most popular authors:')
r2 = pdi.get_data(q2)
print('Days with more than 1% errors:')
r3 = pdi.get_data_probability(q3)
pdi.database_close()
