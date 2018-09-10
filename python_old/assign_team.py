from download_dataset import *
import csv

def assign_team():
    player_team_file=open(TEAM_NAME,"r")
    team_reader=csv.DictReader(player_team_file)


    player_synthesis_file=open(SYNTHESIS_FILE_NAME,"r")
    player_reader=csv.DictReader(player_synthesis_file)

    csvoutput=open(TMP_DATASET_NAME, 'w')

    keys=SYNTHESIS_KEYS
    keys.append("Team")
    writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)

    all=[]
    for player in player_reader:
    	player_team_file.seek(0)
    	for team in team_reader:
    		if player["Name"]==team["Nome"]:
    			player["Team"]=team["Squadra"]
    			break
    	all.append(player)

    writer.writerows(all)

assign_team()