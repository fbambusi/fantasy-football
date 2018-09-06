#mean_evaluation=quotation_log*7.503-5.261
#0.008143*eval^4+4.947492=quote    
from download_dataset import *

import math
def interpolate():
    searchfile=open(SYNTHESIS_QUOTATION_FILE)
    your_csv_file = open(TMP_DATASET_NAME,"w")
    players=csv.DictReader(searchfile)

    keys=SYNTHESIS_KEYS_RECENT
    writer = csv.DictWriter(your_csv_file, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)


    all=[]
    row={}
    for key in keys:
        row[key]=key
    all.append(row)
    print(row)
    for player in players:
    	if player["WeightedFantasyEvaluation"]=="NA":
    		player["WeightedFantasyEvaluation"]=(((float(player["Qt..I"]))-4.947492)/0.008143)
    		if player["WeightedFantasyEvaluation"]<0:
    			player["WeightedFantasyEvaluation"]=0
    		else:
    			player["WeightedFantasyEvaluation"]=player["WeightedFantasyEvaluation"]**0.25
    	if player["Qt..I"]=="NA":
    		player["Plays2018_2019"]=0
    	else:
    		player["Plays2018_2019"]=1
    	all.append(player)
    	print(player["Name"])
    writer.writerows(all)


interpolate()