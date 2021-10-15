'''
	convert.py
	Jake Martens
	14 October 2021

	This file reads in the two CSV files from Kaggle and produces several CSV files
	the form the basis of my SQL database. It is slow, but this is the nature of this
	kind of conversion.
'''

import csv

def main():
	# Convert original NOC regions file into form suitable for SQL database
	with open('noc_regions.csv','r') as noc_regions:
		noc_input = csv.reader(noc_regions)
		noc_dict = {}
		noc_file = open('noc.csv','w')
		noc_writer = csv.writer(noc_file)
		
		ID = 1
		next(noc_input)
		for row in noc_input:
			noc_dict[row[0]] = ID
			# The data here is listed as ['ID','NOC','Region','Notes']
			data = [ID, row[0],row[1],row[2]]
			noc_writer.writerow(data)
			ID += 1

		noc_file.close()

	with open('athlete_events.csv','r') as athlete_events:
		athlete_input = csv.reader(athlete_events)

		# We initialize various main files containing data about individual
		# objects of interest to our queries
		new_athlete_file = open('athletes.csv','w') 
		athlete_writer = csv.writer(new_athlete_file)

		new_games_file = open('games.csv','w')
		games_writer = csv.writer(new_games_file)

		new_medals_file = open('medals.csv','w')
		medals_writer = csv.writer(new_medals_file)

		# Linking table setup - used for processing queries
		athletes_medals = open('athletes_medals.csv','w')
		athletes_medals_writer = csv.writer(athletes_medals)
		athletes_noc = open('athletes_noc.csv','w')
		athletes_noc_writer = csv.writer(athletes_noc)
		athletes_games = open('athletes_games.csv','w')
		athletes_games_writer = csv.writer(athletes_games)
		medals_games = open('medals_games.csv','w')
		medals_games_writer = csv.writer(medals_games)
		medals_noc = open('medals_noc.csv','w')
		medals_noc_writer = csv.writer(medals_noc)


		existing_athletes = set()
		existing_games = {}

		# This long loop transfers relevant data into CSV files
		games_ID = 1
		medal_ID = 1
		next(athlete_input)
		for row in athlete_input:
			athlete_ID = row[0]
			if athlete_ID not in existing_athletes:
				names = row[1].split(' ',1)
				existing_athletes.add(athlete_ID)
				# Data listed as ['ID','Surname', 'Given Name', 'Sex','Age','Height','Weight']
				if len(names) > 1:
					data = [row[0],names[1],names[0],row[2],row[3],row[4],row[5]]
				else:
					data = [row[0],names[0],None,row[2],row[3],row[4],row[5]]
				athlete_writer.writerow(data)
			athletes_noc_writer.writerow([athlete_ID,noc_dict[row[7]]])
			
			year = row[9]
			
			if year not in existing_games:
				# Data listed as ['ID','Year','Season','City']
				data = [games_ID,row[9],row[10],row[11]]
				games_writer.writerow(data)
				existing_games[year] = games_ID
			athletes_games_writer.writerow([athlete_ID,existing_games[year]])
			games_ID += 1

			# Data listed as ['ID','Sport','Event','Medal']
			data = [medal_ID,row[12],row[13],row[14]]
			medals_writer.writerow(data)
			athletes_medals_writer.writerow([athlete_ID,medal_ID])
			medals_noc_writer.writerow([medal_ID,noc_dict[row[7]]])
			medals_games_writer.writerow([medal_ID,existing_games[year]])
			medal_ID += 1

		# We've generated lots of new files, and they all must be closed!
		new_games_file.close()
		new_athlete_file.close()
		new_medals_file.close()
		athletes_medals.close()
		athletes_noc.close()
		athletes_games.close()
		medals_games.close()
		medals_noc.close()


if __name__=='__main__':
	main()
