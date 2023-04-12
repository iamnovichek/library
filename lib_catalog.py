from peewee import *
import uuid
from abc import ABC
import json

# database - SQLite
DB = SqliteDatabase('library.db')


# date manager

class DataManager(ABC):
    def add_book(self, *args, **kwargs):
        pass

    def add_member(self, *args, **kwargs):
        pass

    def delete_member(self, *args, **kwargs):
        pass


class Member(Model):
    member_id = UUIDField(primary_key=True,
                          unique=True,
                          default=uuid.uuid4)
    name = CharField(max_length=60)
    address = CharField(max_length=255)
    email = CharField(max_length=255,
                      unique=True)

    def __str__(self):
        return f'Name: {self.name}, \n' \
               f'Email: {self.email}, \n' \
               f'Address: {self.address} \n'

    class Meta:
        database = DB
        table_name = 'members'


class Book(Model):
    title = CharField(max_length=30)
    author = CharField(max_length=30)
    publisher = CharField(max_length=100)
    ISBN = CharField(max_length=13,
                     primary_key=True,
                     unique=True)
    checked_out = BooleanField(default=False)

    def __str__(self):
        return f'Title: {self.title}\n' \
               f'Author: {self.author}\n'

    class Meta:
        database = DB
        table_name = 'books'


class CheckedOutBook(Model):
    member_id = ForeignKeyField(Member,
                                primary_key=True)
    book_id = ForeignKeyField(Book)

    class Meta:
        database = DB
        table_name = 'checked_out_books'


class CheckOut:
    """Must have check out system"""

    '''it will take a member name and an user email 
       than it will ask an author, after u can ask 
       all books of current author or choose the 
       specific book by entering a title. also
       u can ask a list of popular books'''

    @classmethod
    def _choose_books_by_title(cls, title: str):
        book = Book.select().where(Book.title == title).get()

        return book

    @classmethod
    def _choose_books_by_author(cls, author: str):
        books = Book.select().where(Book.author == author).get()

        return books

    @classmethod
    def _take_member_info(cls,
                          name: str,
                          email: str):
        member = Member.select().where(Member.name == name and Member.email == email).get()

        return member


class Library(DataManager, CheckOut):
    # must have checkout system

    @staticmethod
    def add_book(title: str,  # good
                 author: str,
                 publisher: str,
                 ISBN: int):
        assert len(str(ISBN)) == 13, 'Enter 13 numbers'
        new_book = Book.create(
            title=title,
            author=author,
            publisher=publisher,
            ISBN=ISBN,
            borrowers=0
        )
        new_book.save()

        return new_book

    @staticmethod
    def add_member(name: str,  # good
                   email: str,
                   address: str):
        member = Member.create(
            name=name,
            email=email,
            address=address
        )
        member.save()

        return member

    @staticmethod
    def delete_member(email: str):  # good
        member = Member.get(Member.email == email)
        member.delete_instance()

    @staticmethod
    def list_members():  # good
        all_members = Member.select()

        return all_members

    @staticmethod
    def list_books():  # good
        all_books = Book.select()

        return all_books

    @staticmethod
    def search_book_by_title(title: str):  # good
        book = Book.get(Book.title == title)

        return book

    @staticmethod
    def search_books_by_author(author: str):  # good
        books = Book.select().where(Book.author == author)

        return books

    @classmethod
    def get_popular_books(cls):
        """This method will give 10 latest books checked out"""
        popular_books = CheckedOutBook.select()
        try:
            popular_books = [popular_books[i] for i in range(10)]
        except StopIteration:
            popular_books = [popular_books[i] for i in len(popular_books)]

        return [cls._search_book_by_isbn(book.ISBN) for book in popular_books]

    @staticmethod
    def _search_book_by_isbn(ISBN: int):
        return Book.get(Book.ISBN == ISBN)

    @classmethod
    def get_member_checked_out_books(cls,
                                     email: str):
        member = Member.get(Member.email == email)
        books_id = CheckedOutBook.select('book_id').where(CheckedOutBook.member_id == member.member_id)

        return [cls._search_book_by_isbn(i) for i in books_id]

    @classmethod
    def check_out_specific_book(cls):
        pass

    @classmethod
    def check_out_popular_book(cls):
        pass

    @classmethod
    def check_out_book_by_author(cls):
        pass

    @classmethod
    def return_book(cls,
                    title: str,
                    author: str):
        pass
