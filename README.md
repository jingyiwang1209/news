# About the Analysis Project
## This project gives answers to the following 3 questions.
### 1. What are the most popular three articles of all time?
### 2. Who are the most popular article authors of all time?
### 3. Who are the most popular article authors of all time?

### First, a class called "PythonDatabaseInterface" was created as an interface to connect the database called news, execute and process queries.

### Secondly, 3 queries were created to query the database to get the answers for the 3 questions.
### For the query 1, a view called "subsq" was created to generate a new table with only successful access to the article pages. Then, the column "path" in the log table was formatted (the strings that matched the column "slug" in the articles table were extracted) as a condition for the query. The query shows the title of each article and the number of times readers access to each article, which gives the answer to the 1st question.

### For the query 2, a view called "viewer" was created to hold a table of each author's id and the occurrence of each id, based on query 1. Then the query was created with "viewer" joining the authors table to show the each author's name and the total number of times readers access to all the articles of each author.The query 2 gives the answer to the 2nd question.

### For the query 3, it is required to creat 3 views: "total" representing the time and the summation of all status(failure and succcess), "error" representing the time and summation of failure status, "final" representing the time and the percentage of (occurrence of failure) / (occurence of total). The query makes use of "final" to show the time and only the percentage who is more than 1 %.
