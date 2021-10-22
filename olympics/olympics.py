'''
	olympics.py
	Jake Martens
	21 October 2021

	This command-line program enables the user to access the Olympics
    database implemented in the previous assignment.
'''
import argparse
import psycopg2
from config import database
from config import user
from config import password

def print_all_athletes_from(noc, connection):
    '''Lists the names of all athletes who have
    competed for the specified NOC.
    Connection uses psycopg2 library to specify
    the proper PSQL database.'''
    try:
        cursor = connection.cursor()
        query = '''SELECT DISTINCT athletes.givenname, athletes.surname
            FROM athletes, athletes_noc, noc 
            WHERE athletes.id = athletes_noc.athlete_id 
            AND noc.id = athletes_noc.noc_id 
            AND noc.noc = '{}' 
            ORDER BY athletes.surname;'''.format(noc.upper())
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    # Iterate through rows of cursor to print results of query.
    if cursor.rowcount == 0:
        print('Your query returned no results.')
    else:
        for row in cursor:
            print(row[0], row[1])
        print()

def print_all_medals(connection):
    '''Prints all medals won by each NOC in
    decreasing order of the number of medals.
    Connection uses psycopg2 library to specify
    the proper PSQL database.
    '''
    try:
        cursor = connection.cursor()
        query = '''SELECT noc.noc, COUNT(medals_noc.medal_id)
                FROM noc, medals_noc, medals
                WHERE noc.id = medals_noc.noc_id
                AND medals.id = medals_noc.medal_id
                AND medals.medal = 'Gold'
                GROUP BY noc.noc
                ORDER BY 2 desc;'''
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    # Iterate through rows of cursor to print results of query.
    for row in cursor:
        print(row[0], ':', row[1])
    print()

def print_medals_for(athlete,connection):
    '''Prints all the medals won by athletes
    whose surnames contain the specified string.
    Connection uses psycopg2 library to specify
    the proper PSQL database.'''
    try:
        cursor = connection.cursor()
        query = '''SELECT athletes.givenname, athletes.surname, games.year, medals.medal, medals.sport, medals.event 
                FROM medals, athletes, athletes_medals, medals_games, games
                WHERE medals.id = athletes_medals.medal_id
                AND athletes.id = athletes_medals.athlete_id
                AND medals.medal != 'NA'
                AND medals.id = medals_games.medal_id
                AND games.id = medals_games.games_id
                AND athletes.surname iLIKE '%{}%'
                ORDER BY games.year;'''.format(athlete)
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    # Iterate through rows of cursor to print results of query.
    if cursor.rowcount == 0:
        print('Your query returned no results.')
    else:
        for row in cursor:
            print(row[0], row[1], '-', row[2], row[3], row[4], row[5])
        print()

def main(): 
    # Initialize the parser used in the command line
    parser = argparse.ArgumentParser(usage = 'olympics.py filename [-n [NOC] | [-m] | [-a [SURNAME]] [-h]', \
        description='This command-line program enables the user to retrieve data related to the Olympic games\
            between the years 1896 and 2016. This program relies upon a database designed for the previous assignment.\
            The user may use one flag at a time.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n','--noc', type=str, help='This flag returns the names of all athletes who have competed\
        from the specified NOC. Specify each NOC using its designated IOC code, e.g. POR for Portugal.')
    group.add_argument('-m','--medals', action = 'store_true', help='Lists every NOC and the number of gold medals \
        each has won, in decreasing order of the number of gold medals.')
    group.add_argument('-a','--athlete', type=str, help='Returns all the medals won by athletes whose surnames\
        contain the specified string, sorted by year. Case does not matter. The string should be the desired athlete\'s \
            surname, e.g. "Dunn McKee" returns all medals won by Jonathan Dunn McKee.')

    args = parser.parse_args()

    # Connect to the database
    try:
        connection = psycopg2.connect(database = database, user = user, password = password)
    except Exception as e:
        print(e)
        exit()

    # Check which flag the user has selected and respond accordingly.
    if args.noc:
        print_all_athletes_from(args.noc, connection)
    elif args.medals:
        print_all_medals(connection)
    elif args.athlete:
        print_medals_for(args.athlete,connection)
    else: 
        parser.print_help()

    connection.close()

if __name__ == '__main__':
    main()
