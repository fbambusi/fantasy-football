from download_dataset import *
import csv
import copy

def unwrap():
    player_team_file=open(MANTRA_FILE,"r")
    team_reader=csv.DictReader(player_team_file)

    csvoutput=open(TMP_DATASET_NAME, 'w')

    keys=BID_HEADERS
    writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)

    all=[]
    row={}
    for key in keys:
        row[key]=key
    all.append(row)
    for player in player_reader:
        roles=player["R"].split(";")
        for role in roles:
            pcopy=copy.deepcopy(player)
            pcopy["R"]=role
            all.append(pcopy)

    writer.writerows(all)

unwrap()