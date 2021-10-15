/*  olympics-schema.sql
    Jake Martens
    Jeff Ondich
    14 October 2021

    Statements for creating tables based on CSV files.

    Note that I use text for most entries, even if integer seems more suitable,
    because categories like height or weight frequently contain "NA"
 */

CREATE TABLE athletes (                                                 
id integer,
surname text,
givenname text,
sex text,
age text,
height text,
weight text);
\copy athletes from 'athletes.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE medals (                                                 
id integer,
sport text,
event text,
medal text
);
\copy medals from 'medals.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE games (                                                 
id integer,
year integer,
season text,
city text
);
\copy games from 'games.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE noc (                                                 
id integer,
noc text,
region text,
notes text
);
\copy noc from 'noc.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE athletes_games (
    athlete_id integer,
    games_id integer
);
\copy athletes_games from 'athletes_games.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE athletes_medals (
    athlete_id integer,
    medal_id integer
);
\copy athletes_medals from 'athletes_medals.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE athletes_noc (
    athlete_id integer,
    noc_id integer
);
\copy athletes_noc from 'athletes_noc.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE medals_games (
    medal_id integer,
    games_id integer
);
\copy medals_games from 'medals_games.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE medals_noc (
    medal_id integer,
    noc_id integer
);
\copy medals_noc from 'medals_noc.csv' DELIMITER ',' CSV NULL AS 'NULL'