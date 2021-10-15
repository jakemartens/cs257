/*  queries.sql
    Jake Martens
    Jeff Ondich
    14 October 2021

    SQL Queries for database design assignment
 */

/*
    List all NOCs in alphabetical order by abbreviation
*/
SELECT * FROM noc
    ORDER BY NOC asc;

/*
    List names of all athletes from Kenya by surname

    Note that some surnames may be incorrect as a result of parsing in convert.py
    The main issue is the appearance of extra quotations and nicknames
*/
SELECT DISTINCT athletes.surname, athletes.givenname
    FROM athletes, athletes_noc, noc
    WHERE athletes.id = athletes_noc.athlete_id
    AND noc.id = athletes_noc.noc_id
    AND noc.region = 'Kenya'
    ORDER BY athletes.surname;

/*
    List all the medals won by Greg Louganis, sorted by year.

    Note that I use Louganis's ID to identify him as his name is processed
    incorrectly by convert.py
*/
SELECT games.year, medals.medal, medals.sport, medals.event 
    FROM medals, athletes, athletes_medals, medals_games, games
    WHERE medals.id = athletes_medals.medal_id
    AND athletes.id = athletes_medals.athlete_id
    AND athletes.id = 71665
    AND medals.medal != 'NA'
    AND medals.id = medals_games.medal_id
    AND games.id = medals_games.games_id
    ORDER BY games.year;

/*
    List all the NOCs and the number of gold medals they have won, in decreasing order 
    of the number of gold medals.
*/
SELECT noc.noc, COUNT(medals_noc.medal_id)
    FROM noc, medals_noc, medals
    WHERE noc.id = medals_noc.noc_id
    AND medals.id = medals_noc.medal_id
    AND medals.medal = 'Gold'
    GROUP BY noc.noc
    ORDER BY 2 desc;

