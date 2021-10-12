'''
    books.py
    Chris Melville and Jake Martens, 11 October 2021
    Revised by Jake Martens
    Professor Jeff Ondich

    This command line interface is allows users to 
    works with booksdatasource.py.
'''

import booksdatasource
import argparse

# Prints books contained in the database generated
# from CSV file whose titles contain the string specified
# by the user
def print_matching_titles(title_to_check, database, sort_flag):
    if sort_flag:
        list_of_books = database.books(title_to_check, 'year')
    else:
        list_of_books = database.books(title_to_check)
    for book in list_of_books:
        print(book)

# Prints books contained in the database generated
# from CSV file whose authors contain the string specified
# by the user
def print_matching_authors(author_to_check, database):
    list_of_authors = database.authors(author_to_check)
    for author in list_of_authors:
        print(author)

# Prints books contained in the database generated
# from CSV file whose publications years match those
# specified by the user. Observe that Books object
# handles case where one of the values is None. Moreover, 
# if only one year is specified, the parser assumes it is 
# a start year
def print_books_between_years(start_year, end_year, database):
    list_of_books_between_years = database.books_between_years(start_year, end_year)
    for book in list_of_books_between_years:
        print(book)


def main():
    # Initialize the parser used in the command line
    parser = argparse.ArgumentParser(usage = 'books.py filename [-t [TITLE] [-y] | [-a [AUTHOR]] | [-d DATE DATE]] [-h]', \
        description='The books.py function checks the contents of filename, and returns a sorted list of books matching the \
            criteria specified. Only one of -t, -a, or -d may be used at a time. If more than one is used, the program will throw an error.')
    parser.add_argument('filename', type=str, help='The database to search. This argument is required. The source should be a CSV file.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t','--title',const='', type = str, nargs = '?',help = 'Returns a list of books whose title includes the string inputted\
         by the user, such as "Dark". If TITLE is multiple words, encase it in quotation marks. If no argument specified, returns all books in database.')
    parser.add_argument('-y','--year', action='store_true', help = 'This is an optional flag that only has an effect on --title.\
         When used, books will be sorted according to publication year. Otherwise, defaults to alphabetical order.')
    group.add_argument('-a','--author', const='', type = str, nargs = '?', help = 'Returns a list of books whose author\'s names includes the\
         string inputted by the user, e.g. "Brontë". If AUTHOR is multiple words, encase it in quotation marks. If no author specified, \
             returns all books in database.')
    group.add_argument('-d','--date',nargs='+', type=int, help = 'Returns a list of books whose publication date falls within the range \
        specified by the user in the form "DATE DATE", for example "1948 1996". This flag requires at most two arguments. If only one year\
        is specified, the program returns all books published after that year. Thus, "1996" will return any book published after 1996.')


    args = parser.parse_args()

    # Initialize BooksDataSource object using information
    # contained in specified CSV file
    database = booksdatasource.BooksDataSource(args.filename)

    # Checks which flag is specified by user and calls
    # function to print corresponding data. Observe that
    # each argument is mutually exclusive, so argparse
    # raises error when user specifies too many flags.
    if args.title:
        print_matching_titles(args.title, database, args.year)
    elif args.author:
        print_matching_authors(args.author, database)
    elif args.date:
        if len(args.date) == 1:
            print_books_between_years(args.date[0], None, database)
        elif len(args.date) == 2:
            print_books_between_years(args.date[0], args.date[1], database)
        else:
            raise parser.error('This function requires at most two arguments.')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
