import sqlite3

conn = sqlite3.connect('books.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE books (
        title TEXT,
        author TEXT,
        year INTEGER
    )
''')

conn.commit()
conn.close()
