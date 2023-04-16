from peewee import *
import uuid

# database - SQLite3
DB = SqliteDatabase('library.db')
DB.connect()


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


class CheckOutHistory(Model):
    member_id = UUIDField()
    book_id = ForeignKeyField(Book)

    def __iter__(self):
        cursor = self.select().execute()
        for row in cursor:
            yield row

    class Meta:
        database = DB
        table_name = 'check_out_history'


class CheckedOutBook(Model):
    member_id = UUIDField()
    book_id = ForeignKeyField(Book)
    title = CharField()

    def __iter__(self):
        cursor = self.select().execute()
        for row in cursor:
            yield row

    class Meta:
        database = DB
        table_name = 'checked_out_books'


class CheckOut:
    @classmethod
    def check_out(cls,
                  email: str,
                  title: str,
                  ):
        member = cls._take_member_info(
            email=email
        )
        book = cls._choose_book_by_title(
            title=title
        )

        if not cls._has_current_book(
                member_id=member.member_id,
                book_title=book.title
        ):
            checked_out_book = CheckedOutBook.create(
                member_id=member.member_id,
                book_id=book.ISBN,
                title=book.title
            )
            checked_out_book.save()
            Book.update(checked_out=True).where(
                Book.ISBN == book.ISBN
            ).execute()
            CheckOutHistory.create(
                member_id=member.member_id,
                book_id=book.ISBN
            ).save()

        else:
            raise Exception("You already have this book")

    @classmethod
    def return_book(cls,
                    title: str,
                    email: str):
        member = cls._take_member_info(
            email=email
        )
        book = cls._return_book_by_title(
            title=title
        )

        if cls._has_current_book(
                member_id=member.member_id,
                book_title=title
        ):
            checked_out_book = CheckedOutBook.get(
                member_id=member.member_id,
                title=title
            )
            checked_out_book.delete_instance()
            Book.update(checked_out=False).where(
                Book.ISBN == book.ISBN
            ).execute()
        else:
            raise Exception("You do not have this book")

    @staticmethod
    def _return_book_by_title(title: str):
        try:
            Book.get(Book.title == title)

        except:
            raise Exception("Type correct title")

        try:

            book = Book.select().where(
                Book.title == title,
                Book.checked_out == True
            ).get()

            return book

        except Exception as e:
            raise e

    @staticmethod
    def _choose_book_by_title(title: str):
        try:
            Book.get(Book.title == title)

        except:
            raise Exception("Type correct title")

        try:

            book = Book.select().where(
                Book.title == title,
                Book.checked_out == False
            ).get()

            return book

        except:
            raise Exception("There is not available books for the moment")

    @staticmethod
    def _has_current_book(member_id,
                          book_title
                          ):
        if CheckedOutBook.select().count() == 0:
            return False

        try:
            members = CheckedOutBook.select().where(
                CheckedOutBook.title == book_title
            ).get()

            for member in members:
                if member.member_id == member_id and member.title == book_title:

                    member = CheckedOutBook.select().where(
                        CheckedOutBook.member_id == member_id
                    ).get()

                    for m in member:
                        if m.title == book_title:
                            return True

            return False

        except:
            return False

    @staticmethod
    def _choose_book_by_author(author: str):
        return Book.select().where(
            Book.author == author
        ).get()

    @staticmethod
    def _take_member_info(email: str):
        try:
            return Member.get(
                Member.email == email
            )
        except:
            raise Exception("Type correct email")


class Library:

    @staticmethod
    def add_book(title: str,
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
    def add_member(name: str,
                   email: str,
                   address: str):
        new_member = Member.create(
            name=name,
            email=email,
            address=address
        ).save()

        return new_member

    @staticmethod
    def delete_member(email: str):
        member = Member.get(Member.email == email)
        member.delete_instance()

    @staticmethod
    def check_out(member_email: str,
                  book_title: str):
        CheckOut.check_out(
            email=member_email,
            title=book_title
        )

    @staticmethod
    def return_book(member_email: str,
                    book_title: str):
        CheckOut.return_book(
            title=book_title,
            email=member_email
        )

    @staticmethod
    def list_members():
        return Member.select()

    @staticmethod
    def list_books():
        return Book.select()

    @staticmethod
    def search_book_by_title(title: str):
        return Book.get(Book.title == title)

    @staticmethod
    def search_books_by_author(author: str):
        return Book.select().where(Book.author == author)

    @classmethod
    def get_popular_books(cls):
        """Returns 10 last checked out books"""

        if CheckOutHistory.select().count() == 0:
            raise Exception("Nobody have not checked out book yet")

        if CheckOutHistory.select().count() < 10:
            books = CheckOutHistory.select().order_by(
                CheckOutHistory.id.desc()
            )

            return [Book.get(Book.ISBN == book.book_id) for book in books]

        if CheckOutHistory.select().count() >= 10:
            books = CheckOutHistory.select().order_by(
                CheckOutHistory.id.desc()
            ).limit(10)

            return [Book.get(Book.ISBN == book.book_id) for book in books]

    @staticmethod
    def _search_book_by_isbn(ISBN: int):
        return Book.get(Book.ISBN == ISBN)

    @classmethod
    def get_member_checked_out_books(cls,
                                     email: str):

        try:
            member = Member.get(Member.email == email)
            if CheckedOutBook.select().where(
                    CheckedOutBook.member_id == member.member_id
            ).count() == 0:
                raise Exception("You have not checked out any book yet")

            books = CheckedOutBook.select().where(
                CheckedOutBook.member_id == member.member_id
            )

            return [cls._search_book_by_isbn(book.book_id) for book in books]

        except Exception as e:
            raise f"{e} - type correct email"
