from download_dataset import *
from operator import itemgetter
BONUS_GOAL=3
MALUS_GOAL=-1
BONUS_ASSIST=1
SCORED_PENALTY_BONUS=3
SAVED_PENALTY_BONUS=3
MISSED_PENALTY_MALUS=-3

import csv
import csv


searchfile=open(PLAYER_SYNTHESIS)
your_csv_file = open(TMP_DATASET_NAME,"w")
players=csv.DictReader(searchfile)

keys=SYNTHESIS_KEYS_RECENT
writer = csv.DictWriter(your_csv_file, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)


all=[]
row={}
for key in keys:
    row[key]=key
all.append(row)

players = sorted(players, key=itemgetter('WeightedFantasyEvaluation'),reverse=True) 

#all.append(keys)
played=33
for row in players:
    if row["PlayedMatches"]=="NA":
        row["PlayedMatches"]=played
    played=row["PlayedMatches"]
    all.append(row)

writer.writerows(all)