from download_dataset import *
import csv

def assign_team():
   


    player_synthesis_file=open(PLAYER_SYNTHESIS,"r")
    player_reader=csv.DictReader(player_synthesis_file)

    csvoutput=open(TMP_DATASET_NAME, 'w')

    keys=SYNTHESIS_KEYS_WEIGHTED
    writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)

    all=[]
    row={}
    for key in keys:
        row[key]=key
    all.append(row)

    for player in player_reader:
        print(player)
        player["WeightedFantasyEvaluation"]=float(player["MeanFantasyEvaluation"])*float(player["PlayedMatches"])/38
        all.append(player)

    writer.writerows(all)

assign_team()