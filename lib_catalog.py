from peewee import *

# date manager

# database - SQLite
DB = SqliteDatabase('library.db')


class MemberModel(Model):
    user_id = AutoField(primary_key=True,
                        unique=True)
    name = CharField(max_length=60)
    address = CharField(max_length=255)
    email = CharField(max_length=255)

    class Meta:
        database = DB
        table_name = 'members'


class CheckedOutBookModel(Model):
    user_id = ForeignKeyField(MemberModel)


    class Meta:
        database = DB
        table_name = 'checked_out_books'


class BookModel(Model):
    book_id = AutoField(primary_key=True,
                        unique=True)
    title = CharField(max_length=30)
    author = CharField(max_length=30)
    publisher = CharField(max_length=100)
    ISBN = CharField(max_length=13)
    checked_out = BooleanField()

    class Meta:
        database = DB
        table_name = 'books'


class DataManager:

    def add_book(self, book: object,
                 quantity: int = 1):
        pass

    def add_member(self, member: object):
        pass

    def find_member_by_id(self):
        pass

    def delete_member(self, member: object):
        pass


class Book:
    # I think It's done
    def __init__(self,
                 TITLE: str,
                 AUTHOR: str,
                 PUBLISHER: str,
                 ISBN: int,
                 borrowers: list = None
                 ):
        self.title = TITLE
        self.author = AUTHOR
        self.publisher = PUBLISHER

        # must have 13 ints
        self.ISBN = ISBN
        self.borrowers = borrowers

    def __str__(self):
        return f'Name: {self.title}/ Author: {self.author}'

    def __repr__(self):
        return f'Book(TITLE="{self.title}", ' \
               f'AUTHOR="{self.author}", ' \
               f'PUBLISHER="{self.publisher}", ' \
               f'borrowers="{self.borrowers}")'


class Library:
    # must have checkout system
    _db = DataManager()
    books = []
    members = []

    @classmethod
    def add_book_to_db(cls,
                       title: str,
                       author: str,
                       publisher: str,
                       ISBN: int):
        assert len(str(ISBN)) == 13, 'Enter 13 numbers'
        new_book = Book(
            TITLE=title,
            AUTHOR=author,
            PUBLISHER=publisher,
            ISBN=ISBN
        )

        cls._db.add_book(new_book)

        return new_book

    @classmethod
    def create_new_member(cls,
                          name,
                          email,
                          address):
        new_member = Member(
            name=name,
            email=email,
            address=address
        )

        cls._db.add_member(new_member)

        return new_member

    def delete_member(self):
        pass

    def check_out(self):
        pass

    def return_book(self):
        pass

    def list_books(self):
        pass

    def search_by_title(self, title: str):
        pass

    def search_by_author(self, author: str):
        pass

    def get_popular_books(self):
        """This method will give 10 books"""
        pass

    def get_number_of_books(self, book_id: int):
        pass


class Member:

    def __init__(self,
                 name: str,
                 email: str,
                 address: str,
                 books_checked_out: list = None):
        self.name = name
        self.email = email
        self.address = address
        self.books_checked_out = books_checked_out

    def __str__(self):
        return f'Member: {self.name}'

    def __repr__(self):
        return f'Member(name="{self.name}", ' \
               f'email="{self.email}", ' \
               f'address="{self.address}",' \
               f'books_checked_out="{self.books_checked_out}")'

    def get_books_checked_out(self):
        pass


class CheckOut:
    """Must have check out system"""
