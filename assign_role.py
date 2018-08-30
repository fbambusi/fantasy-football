from download_dataset import *
import csv

def assign_team():
    player_team_file=open(BASIC_FANGAZZETTA_EVALUATIONS,"r")
    team_reader=csv.DictReader(player_team_file)


    player_synthesis_file=open(SYNTHESIS_FILE_NAME,"r")
    player_reader=csv.DictReader(player_synthesis_file)

    csvoutput=open(TMP_DATASET_NAME, 'w')

    keys=SYNTHESIS_KEYS_ROLE
    writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)

    all=[]
    row={}
    for key in keys:
        row[key]=key
    all.append(row)
    for player in player_reader:
    	player_team_file.seek(0)
    	for team in team_reader:
    		if player["Name"]==team["Nome"]:
    			player["Role"]=team["R"]
    			break
    	all.append(player)

    writer.writerows(all)

assign_team()