from peewee import *
from lib_catalog import *


DB.connect()


books = Library.search_books_by_author(
    author="Lol"
)

for book in books:
    print(book)