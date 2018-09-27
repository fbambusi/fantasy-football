from download_dataset import *


import csv
import csv

BONUS_GOAL=3
MALUS_GOAL=-1
BONUS_ASSIST=1
SCORED_PENALTY_BONUS=3
SAVED_PENALTY_BONUS=3
MISSED_PENALTY_MALUS=-3

def main():
    with open(FULL_DATASET_NAME,'r') as csvinput:
        print("Opening file      "+FULL_DATASET_NAME)
        with open(TMP_DATASET_NAME, 'w') as csvoutput:
            keys=SINGLE_EVALUATION_KEYS
            writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)

            reader = csv.DictReader(csvinput)

            all = []
            row={}
            for key in keys:
                row[key]=key
            all.append(row)

            for row in reader:
                fantasy_evaluation=float(row["Voto"])+BONUS_GOAL*float(row['Gf'])+MALUS_GOAL*float(row['Gs'])+BONUS_ASSIST*float(row['Ass'])
                fantasy_evaluation+=SAVED_PENALTY_BONUS*float(row["Rp"])
                fantasy_evaluation+=MISSED_PENALTY_MALUS*float(row["Rs"])
                fantasy_evaluation+=SCORED_PENALTY_BONUS*float(row["Rf"])
                row["FantasyEvaluation"]=fantasy_evaluation
                all.append(row)

            writer.writerows(all)




if __name__ == "__main__":
    main()