# About the Analysis Project
## This project gives answers to the following 3 questions.
### 1. What are the most popular three articles of all time?
### 2. Who are the most popular article authors of all time?
### 3. Who are the most popular article authors of all time?

## How to load the connect to the database news and run the python code
### 1. Once newsdata.sql is downloaded, run ```psql -d news -f newsdata.sql``` at your terminal to connect to the databse news and run the SQL statement in the newsdata.sql
### 2. Run ```psql -d news``` to look at the details of the database news.
### 3. Run ```\q``` to exit the database news and run ```python newsdb.py```. Your terminal will show the results of the quries.

### First, a class called "PythonDatabaseInterface" was created as an interface to connect the database called news, execute and process queries.

### Secondly, 3 queries were created to query the database to get the answers for the 3 questions.

### A view function needs to be created for the efficient use of query 1:
```
subsq = "create view subsq as select path, count(*) as nums from public.log "\
        "where status = '200 OK' group by path order by nums desc;"
```

### For the query 1, a view called "subsq" above should be created to generate a new table with only successful access to the article pages. Then, the column "path" in the log table is formatted (the strings that matched the column "slug" in the articles table were extracted) as a condition for the query. The query shows the title of each article and the number of times readers access to each article, which gives the answer to the 1st question.

### A view function needs to be created for the efficient use of query 2:
[comment]: (Use 'left join' just for the extreme case which is probably very rare in reality: some author's all articles have not been read by any reader.)
```
viewer = "create view viewer as select public.articles.author, "\
         "sum(nums) as nums from public.articles left join subsq "\
         "on public.articles.slug = " + formatted_path +\
         "group by public.articles.author;"\
```
### For the query 2, a view called "viewer" above should be created to hold a table of each author's id and the total occurrences of each id. Then the query can be created with "viewer" joining the authors table to show each author's name and the total number of times readers access to all the articles of each author. The query 2 gives the answer to the 2nd question.

### Some view functions need to be created for the efficient use of query 3:
```
view_total = "create view total as select time::timestamp::date, "\
             "count(status) as total_count from public.log "\
             "group by time::timestamp::date;"

view_error = "create view errors as select time::timestamp::date, "\
             "count(status) as error_count from public.log "\
             "where not status = '200 OK' group by time::timestamp::date;"

view_final = "create view final as select total.time, "\
             "(errors.error_count::float /total.total_count::float)"\
             "*100 as prob from total right join errors "\
             "on total.time = errors.time;"
```

### For the query 3, it is required to creat 3 views as above: "total" representing the time and the summation of all status(failure and succcess), "error" representing the time and summation of failure status, "final" representing the time and the percentage of (occurrence of failure) / (occurence of total). The query makes use of "final" to show the time and only the percentage who is more than 1 %.
