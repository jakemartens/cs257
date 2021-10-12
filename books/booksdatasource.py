#!/usr/bin/env python3
# Authors: Chris Melville and Jake Martens

'''
    books.py
    Chris Melville and Jake Martens, 11 October 2021
    Professor Jeff Ondich

    For use in the 'books' assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.

    Revised by Jake Martens
'''

import csv
import re

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __str__(self):
        if self.death_year is None:
            return (self.surname + ', ' + self.given_name + ' ' + str(self.birth_year) + '-present')
        else:
            return (self.surname + ', ' + self.given_name + ' ' + str(self.birth_year) + '-' + str(self.death_year))

    # This function was necessary for implementing __eq__() function
    def __hash__(self):
        return id(self)

    def __eq__(self, other_author):
        return str(self) == str(other_author)

    #Check if an author's name contains a given string, ignoring case
    def contains_string(self, string_to_check):
        author_name = self.given_name + ' ' + self.surname
        match = re.search(string_to_check, author_name, re.IGNORECASE)

        if match is not None:
            return True
        else:
            return False

    # Returns author's name. For use in booksdatasourcetests.py
    def get_author_name(self):
        return self.given_name + ' ' + self.surname

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __str__(self):
        author_string = str(self.authors[0])

        for i in range (1, len(self.authors)):
            author_string += ' and '+ str(self.authors[i])

        return '{} ({}) by {}'.format(self.title, self.publication_year, author_string)

    # Returns a book's title. For use in booksdatasourcetests.py
    def get_title(self):
        return self.title

    #Check if a book's name contains a given string, ignoring case
    def contains_string(self, string_to_check):
        book_name = self.title
        match = re.search(string_to_check, book_name, re.IGNORECASE)

        if match is not None:
            return True
        else:
            return False

    # Returns publication year of a book. For use in booksdatasourcetests.py
    def get_publication_year(self):
        return self.publication_year

    # Checks if a book was published between given years. If start_year or end_year is None, assumes True
    def is_between_years(self, start_year, end_year):
        if start_year is not None and end_year is not None:
            if self.publication_year >= start_year and self.publication_year <= end_year:
                return True
        elif start_year is None and end_year is None:
            return True
        elif start_year is None and self.publication_year <= end_year:
            return True
        elif end_year is None and self.publication_year >= start_year:
            return True
        else:
            return False

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.books_set = set()
        self.authors_set = set()
        self.load_data_from_csv(books_csv_file_name)

    # This lengthy function process data contained in CSV file
    # and creates a set containing Book objects for books
    # contained therein, as well as a set containing an Author
    # object for each author referenced in file.
    def load_data_from_csv(self, books_csv_file_name):
        # These indices are used in the messy process of string-processing
        # They are included purely for clarity
        TITLE_INDEX = 0
        PUBLICATION_YEAR_INDEX= 1
        AUTHORS_INDEX = 2
        GIVEN_NAME_INDEX = 0
        SURNAME_FROM_LIST_INDEX = 1
        SURNAME_INDEX = 0
        YEAR_INDEX = 1

        with open(books_csv_file_name,'r') as csv_file:
            for row in csv.reader(csv_file):
                curr_title = row[TITLE_INDEX]
                curr_publication_year = int(row[PUBLICATION_YEAR_INDEX])
                authors_of_book = []
                curr_authors = row[AUTHORS_INDEX].split(' and ')
                for author in curr_authors:
                    list_for_given_name = author.split(' ',1)
                    given_name = list_for_given_name[GIVEN_NAME_INDEX]
                    list_for_surname = list_for_given_name[SURNAME_FROM_LIST_INDEX].split(' (')
                    surname = list_for_surname[SURNAME_INDEX]
                    birth_year = int(list_for_surname[YEAR_INDEX][0:4])
                    death_year = None
                    if len(list_for_surname[YEAR_INDEX]) > 8:
                        death_year = int(list_for_surname[YEAR_INDEX][5:9])
                    author_as_object=Author(surname, given_name, birth_year, death_year)

                    if self.check_if_in_set(author_as_object) is not None:
                        author_as_object = self.check_if_in_set(author_as_object)
                    else:
                        self.authors_set.add(author_as_object)

                    authors_of_book.append(author_as_object)

                curr_book = Book(curr_title, curr_publication_year, authors_of_book)
                self.books_set.add(curr_book)

    # Checks if an Author object already exists in the
    # the set containing for an author in CSV file.
    # This function is called by load_data_from_csv()
    def check_if_in_set(self, author_to_check):
        for author in self.authors_set:
            if author == author_to_check:
                return author
        return None

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        if search_text == None:
            search_text = ''

        authors_that_match = []
        for author in self.authors_set:
            if author.contains_string(search_text):
                authors_that_match.append(author)

        authors_that_match.sort(key = lambda book: str(book))

        return authors_that_match

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        if search_text == None:
            search_text = ''

        books_that_match = []
        for book in self.books_set:
            if book.contains_string(search_text):
                books_that_match.append(book)

        if sort_by == 'year':
            books_that_match.sort(key = lambda book: book.get_publication_year())
        else:
            books_that_match.sort(key = lambda book: str(book))

        return books_that_match

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        books_that_match = []
        for book in self.books_set:
            if book.is_between_years(start_year, end_year):
                books_that_match.append(book)

        books_that_match.sort(key = lambda book: (book.get_publication_year(), str(book)))
        return books_that_match
