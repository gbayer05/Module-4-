import csv
import sqlite3

conn = sqlite3.connect('books.db')
cur = conn.cursor()

with open('books2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute('INSERT INTO books VALUES (?, ?, ?)',
                    (row['title'], row['author'], row['year']))

conn.commit()
conn.close()

#sorting the books order by title 
import sqlite3

conn = sqlite3.connect('books.db')
cur = conn.cursor()

for row in cur.execute('SELECT title FROM books ORDER BY title'):
    print(row[0])

conn.close()
#sorting the books order by the year 
import sqlite3

conn = sqlite3.connect('books.db')
cur = conn.cursor()

for row in cur.execute('SELECT * FROM books ORDER BY year'):
    print(row)

conn.close()
#soting the books order by title
import sqlite3

conn = sqlite3.connect('books.db')
cur = conn.cursor()

for row in cur.execute('SELECT * FROM books ORDER BY title'):
    print(row)

conn.close()