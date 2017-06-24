# "Database code" for interfacing with the DB News.

import psycopg2

class PythonDatabaseInterface:
    """The class contains several methods of connecting, closing a database and processing a query."""
    
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
            print(row[0]+' - '+str(row[1]) + ' views')
   
    def get_data(self, query):       
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.print_helper(rows)

    def get_data_probability(self, query):       
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            print(str(row[0])+' - '+str(row[1]) + '% errors')

    def database_close(self):
        self.cursor.close()
        self.conn.close()

    
 


# Extract the number of views with only successul request and response
view = "create view subsq as select * from public.log where status = '200 OK'; "

# Extract the string equals to slug from path
formatted_path = "(regexp_split_to_array(subsq.path, E'/article/'))[2]"

q1 = view+"select public.articles.title, count(*) as nums from public.articles join subsq on public.articles.slug = "+formatted_path+" group by public.articles.title order by nums desc limit 3;"

# Use 'left join' just for the extreme case which is probably very rare in reality:
# some author's all articles have not been read by any reader.
q2 = "create view viewer as select public.articles.author, count(subsq.id) as nums from public.articles left join subsq on public.articles.slug = "+formatted_path+" group by public.articles.author; \
select public.authors.name, viewer.nums from public.authors, viewer where public.authors.id = viewer.author order by viewer.nums desc;"


# Extract a table with time and total amount of all status(success and failure)
view_total= "create view total as select time::timestamp::date, count(status) as total_count from public.log group by time::timestamp::date;"
# Extract a table with time and total amount of failure status
view_error= "create view errors as select time::timestamp::date, count(status) as error_count from public.log where not status = '200 OK' group by time::timestamp::date;"
# Join into a table with time and percentage of failure status / total status
view_final = "create view final as select total.time, (errors.error_count::float /total.total_count::float)*100 as prob from total right join errors on total.time = errors.time;"
# Only show the rows whose percentage is more than 1 %
q3 = view_total + view_error + view_final + "select time, prob from final where prob > 1"

pdi = PythonDatabaseInterface("dbname=news")
r1 = pdi.get_data(q1)
r2 = pdi.get_data(q2)
r3 = pdi.get_data_probability(q3)
pdi.database_close()





