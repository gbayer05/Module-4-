import csv

with open('books.csv', newline='') as csvfile:
    books = csv.DictReader(csvfile)
    for book in books:
        print(book)
