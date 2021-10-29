#!/usr/bin/env python3
'''
    olympics-api.py
    Jake Martens
    Professor Jeff Ondich
    27 October 2021

    This Flask-based application is an implementation of an API based on the Olympics database
    created for the previous assignment.
'''
import sys
import argparse
import flask
import json
import psycopg2
from config import database
from config import user
from config import password

app = flask.Flask(__name__)

# Connect to database, global variable as it is used in every function
try:
    connection = psycopg2.connect(database = database, user = user, password = password)
except Exception as e:
    print(e)
    exit()

@app.route('/games')
def get_games():
    ''' Returns a JSON list of dictionaries, each of which represents one
    Olympic games, sorted by year. Each dictionary in this list contains 
    fields for ID, year, season, and city.'''
    try:
        cursor = connection.cursor()
        query = '''SELECT * FROM games
                ORDER BY year'''
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    game_list = []
    for game in cursor:
        game_entry = {'id':game[0], 'year':game[1], 'season':game[2], 'city':game[3]}
        game_list.append(game_entry)

    return json.dumps(game_list)

@app.route('/nocs')
def get_nocs():
    '''Returns a JSON list of dictionaries, each of which represents one
    National Olympic Committee, alphabetized by NOC abbreviation. Each dictionary
    in this list contains fields for NOC abbreviation and region name.'''
    try:
        cursor = connection.cursor()
        query = '''SELECT noc, region FROM noc
                ORDER BY noc asc'''
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    noc_list = []
    for noc in cursor:
        noc_entry = {'abbreviation':noc[0], 'name':noc[1]}
        noc_list.append(noc_entry)

    return json.dumps(noc_list)

@app.route('/medalists/games/<games_id>')
def get_medalist(games_id):
    '''Returns a JSON list of dictionaries, each representing one athlete
    who earned a medal in the specified games. Each dictionary contains 
    fields for athlete ID, athlete name, athlete sex, sport, medal
    and event.'''
    # noc allows us to access NOC endpoint data if /medalists/games/<games_id>?[noc=noc_abbreviation]
    # is specified
    noc = flask.request.args.get('noc')

    if noc is not None: # Case where NOC is specified
        noc = noc.upper()
        query = '''SELECT DISTINCT athletes.id, athletes.givenname, athletes.surname, athletes.sex, medals.sport, medals.event, medals.medal
                FROM athletes, medals, athletes_medals, medals_games, noc, athletes_noc
                WHERE athletes.id = athletes_medals.athlete_id
                AND medals.id = athletes_medals.medal_id
                AND medals.medal != 'NA'
                AND medals.id = medals_games.medal_id
                AND medals_games.games_id = {}
                AND athletes.id = athletes_noc.athlete_id
                AND noc.id = athletes_noc.noc_id
                AND noc.noc = '{}';'''.format(games_id, noc)
    else: # Case where NOC is unspecified
        query = '''SELECT athletes.id, athletes.givenname, athletes.surname, athletes.sex, medals.sport, medals.event, medals.medal
                    FROM athletes, medals, athletes_medals, medals_games
                    WHERE athletes.id = athletes_medals.athlete_id
                    AND medals.id = athletes_medals.medal_id
                    AND medals.medal != 'NA'
                    AND medals.id = medals_games.medal_id
                    AND medals_games.games_id = {};'''.format(games_id)
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    medalist_list = []
    for medalist in cursor:
        name = medalist[1] + ' ' + medalist[2]
        medalist_entry = {'athlete_id':medalist[0], 'athlete_name':name, 'athlete_sex':medalist[3],
        'sport':medalist[4], 'event':medalist[5], 'medal':medalist[6]}

        medalist_list.append(medalist_entry)

    return json.dumps(medalist_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('This Flask-based application is an implementation of an API\
        based on an Olympics database.')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)

    
