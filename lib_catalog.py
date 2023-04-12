from peewee import *
from abc import ABC
import json

# date manager

# database - SQLite
DB = SqliteDatabase('library.db')


# DB.connect()
# DB.create_tables(['members', 'books', 'checked_out_books'])

class DataManager(ABC):
    def add_book(self, *args, **kwargs):
        pass

    def add_member(self, *args, **kwargs):
        pass

    def delete_member(self, *args, **kwargs):
        pass


class Member(Model):
    member_id = AutoField(primary_key=True,
                          unique=True)
    name = CharField(max_length=60)
    address = CharField(max_length=255)
    email = CharField(max_length=255,
                      unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        database = DB
        table_name = 'members'


class Book(Model):
    book_id = AutoField(primary_key=True,
                        unique=True)
    title = CharField(max_length=30)
    author = CharField(max_length=30)
    publisher = CharField(max_length=100)
    ISBN = CharField(max_length=13)
    # checked_out = BooleanField() --> to do
    borrowers = TextField()  # will be a json array

    def __str__(self):
        return f'Title: {self.title}/ Author: {self.author}'

    class Meta:
        database = DB
        table_name = 'books'


class CheckedOutBook(Model):
    user_id = ForeignKeyField(Member, backref='member_id')
    book_id = ForeignKeyField(Book)

    class Meta:
        database = DB
        table_name = 'checked_out_books'


class Library(DataManager):
    # must have checkout system

    @classmethod
    def add_book(cls,
                 title: str,
                 author: str,
                 publisher: str,
                 ISBN: int):
        assert len(str(ISBN)) == 13, 'Enter 13 numbers'
        book = Book.create(
            title=title,
            author=author,
            publisher=publisher,
            ISBN=ISBN,
            borrowers=None
            # my_list = ['item 1', 'item 2', 'item 3']
            # json_data = json.dumps(my_list)
        )
        book.save()

        return book

    @classmethod
    def add_member(cls,
                   name: str,
                   email: str,
                   address: str):
        member = Member.create(
            name=name,
            email=email,
            address=address
        )
        member.save()

        return member

    @classmethod
    def delete_member(cls, email: str):
        member = Member.select().where(Member.email == email).get()
        member.delete_instance()

        return member

    @classmethod
    def list_members(cls):
        all_members = Member.select()

        return all_members

    @classmethod
    def list_books(cls):
        all_books = Book.select('title', 'author')

        return all_books

    @classmethod
    def search_book_by_title(cls, title: str):
        book = Book.select('title').where(Book.title == title).get()

        return book

    @classmethod
    def search_books_by_author(cls, author: str):
        books = Book.select('author').where(Book.author == author).get()

        return books

    @classmethod
    def get_popular_books(cls):
        """This method will give 10 latest books checked out"""
        popular_books_id = CheckedOutBook.select('book_id')[0:11]
        popular_books = []
        for book in len(popular_books_id):
            popular_books.append(
                Book.select('title', 'author').where(Book.book_id == book).get()
            )

        return popular_books

    @classmethod
    def get_member_checked_out_books(cls, email):
        members_id = CheckedOutBook.select('member_id')
        for id in members_id:
            member = Member.get(Member.member_id == id)
            if member.email == email:
                books = CheckedOutBook.select('book_id').where(CheckedOutBook.member_id == id).get()
                return books

    def check_out(self):
        pass

    def return_book(self):
        pass


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
