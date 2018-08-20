from download_dataset import *
BONUS_GOAL=3
MALUS_GOAL=-1
BONUS_ASSIST=1

import csv
import csv

with open(FULL_DATASET_NAME,'r') as csvinput:
    with open(TMP_DATASET_NAME, 'w') as csvoutput:
        keys=SINGLE_EVALUATION_KEYS
        keys.append("FantasyEvaluation")
        writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)

        reader = csv.DictReader(csvinput)

        all = []
        #all.append(keys)

        for row in reader:
            fantasy_evaluation=float(row["Voto"])+BONUS_GOAL*float(row['Gf'])+MALUS_GOAL*float(row['Gs'])+BONUS_ASSIST*float(row['Ass'])
            row["FantasyEvaluation"]=fantasy_evaluation
            all.append(row)

        writer.writerows(all)