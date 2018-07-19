import re
import operator
from typing import Union, Dict, List, Hashable

class User(object):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print('User email was changed to: {}'.format(self.email))

    def __repr__(self):
        return 'user: {}, email: {}, books read: {}, average rating: {:.2f}'.format(self.name, self.email, str(len(self.books)), self.rating)

    def __eq__(self, other_user: 'User') -> bool:
        return self.name == other_user.name & self.email == other_user.email

    def read_book(self, book: 'Book', rating: Union[int, float] = None):
        self.books[book] = rating
        self.rating = self.get_average_rating()
        self.count = len(self.books)
        self.total_price = sum(book.price for book in self.books)

    def get_average_rating(self) -> float:
        ratings = [rating for rating in self.books.values() if rating]
        if ratings:
            return float(sum(ratings) / len(ratings))

class Book(object):

    def __init__(self, title: str, isbn: int, price: float):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("This book's ISBN has been updated.")

    def add_rating(self, rating: Union[int, float] = None):
        if rating and rating > 0 and rating <= 4:
            self.ratings.append(float(rating))
            self.average_rating = self.get_average_rating()
            print('A rating of {:.2f} was added to {} with a total of {} ratings and an average rating of {:.2f}'.format(rating, self.title, str(len(self.ratings)), self.average_rating))
        else:
            print('Invalid Rating')

    def __eq__(self, other_book):
        if self.title == other_book.title & self.isbn == other_book.isbn:
            return True
        else:
            return False

    def get_average_rating(self) -> float:
        if self.ratings:
            return float(sum(self.ratings) / len(self.ratings))
        return 0

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):

    def __init__(self, title: str, author: str, isbn: int, price: float):
        Book.__init__(self, title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self) -> str:
        return '{} by {} with ISBN {} has an average rating of {:.2f}'.format(self.title, self.author, self.isbn,
                                                                              self.average_rating)


class Non_Fiction(Book):

    def __init__(self, title: str, subject: str, level: str, isbn: int, price: float):
        Book.__init__(self, title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return self.title + ", a " + self.level + " manual on " + self.subject


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}
        self.library = {}

    def __repr__(self) -> str:
        return 'TomeRater has {} users and {} books'.format(len(self.users), len(self.books))

    def __eq__(self, other_tomerater: 'TomeRater') -> bool:
        return self.users == other_tomerater.users and self.books == other_tomerater.books

    def create_book(self, title: str, isbn: int, price: float = 0.00) -> 'Book':
        if isbn not in self.library:
            new_book = Book(title, isbn, price)
            self.library[isbn] = new_book
            print('Add {} with ISBN {} to TomeRater'.format(title, isbn))
            return new_book
        else:
            print('{} not added, a book with ISBN {} already exists!'.format(title, isbn))
            return None

    def create_novel(self, title: str, author: str, isbn: int, price: float = 0.00) -> 'Fiction':
        if isbn not in self.library:
            new_novel = Fiction(title, author, isbn, price)
            self.library[isbn] = new_novel
            print('Add {} with ISBN {} to TomeRater'.format(title, isbn))
            return new_novel
        else:
            print('{} not added, a book with ISBN {} already exists!'.format(title, isbn))
            return None

    def create_non_fiction(self, title: str, subject: str, level: str, isbn: int, price: float = 0.00) -> 'Non_Fiction':
        if isbn not in self.library:
            new_non_fiction = Non_Fiction(title, subject, level, isbn, price)
            self.library[isbn] = new_non_fiction
            print('Add {} with ISBN {} to TomeRater'.format(title, isbn))
            return new_non_fiction
        else:
            print('{} not added, a book with ISBN {} already exists!'.format(title, isbn))
            return None

    def add_book_to_user(self, book: 'Book', email: str, rating: Union[int, float] = None):
        user = self.users.get(email)
        if book:
            try:
                user.read_book(book, rating)
                if book not in self.books:
                    self.books[book] = 0
                self.books[book] += 1
                book.add_rating(rating)
            except ValueError:
                print('No user with email {}'.format(email))

    def add_user(self, name: str, email: str, user_books: Dict['Book', Union[int, float]] = None):
        if not email in self.users and self.validate_email(email):
            new_user = User(name, email)
            self.users[email] = new_user
            if user_books:
                for book in user_books:
                    self.add_book_to_user(book, email)
        else:
            print('You entered an invalid email {email}!'.format(email=email))

    def validate_email(self, email: str) -> bool:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users.values:
            print(user)

    def most_read_book(self) -> List['Books']:
        if self.books:
            max_read = max(self.books.values())
            return list(k for k, v in self.books.items() if v == max_read)
        return None


    def highest_rated_book(self):
        if self.books:
            max_rating = max(k.average_rating for k in self.books.keys())
            return list(k for k in self.books.keys() if k.average_rating == max_rating)
        return None

    def most_positive_user(self):
        if self.users:
            max_user = max(v.rating for v in self.users.values())
            return list(v for v in self.users.values() if v.rating == max_user)
        return None
