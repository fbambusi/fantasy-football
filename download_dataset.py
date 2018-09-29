import urllib.request
import xlrd
import csv
import os
import csv

EXCEL_NAME="dataset/day"
CSV_NAME="dataset/day"
FULL_DATASET_NAME="dataset/all_days2.csv"
DAYS="dataset/all_days_with_fantasy_evaluation.csv"
TMP_DATASET_NAME="dataset/all_days_tmp.csv"
BASIC_FANGAZZETTA_EVALUATIONS="dataset/quotazioni.csv"
PLAYER_SYNTHESIS="dataset/players_synthesis_by_me.csv"
TEAM_NAME="dataset/player_teams.csv"
SYNTHESIS_FILE_NAME="dataset/players_with_fantasy_evaluation.csv"
SYNTHESIS_QUOTATION_FILE="dataset/synthesis_with_quotations.csv"
MANTRA_FILE="dataset/Quotazioni_Fantacalcio_Ruoli_Mantra.csv"


SHEET_NAME="Fantagazzetta"
HEADERS='"Cod.","Ruolo","Nome","Voto","Gf","Gs","Rp","Rs","Rf","Au","Amm","Esp","Ass","Asf","Gdv","Gdp","Day","FantasyEvaluation","Year"'
SINGLE_EVALUATION_KEYS=["Cod.","Ruolo","Nome","Voto","Gf","Gs","Rp","Rs","Rf","Au","Amm","Esp","Ass","Asf","Gdv","Gdp","Day","Year","FantasyEvaluation"]
DAILY_KEYS=SINGLE_EVALUATION_KEYS
DAILY_KEYS.append("Delta")


SYNTHESIS_KEYS=["Name","VarianceFantasyEvaluation","PlayedMatches","MeanFantasyEvaluation"]
SYNTHESIS_KEYS_ROLE=SYNTHESIS_KEYS
SYNTHESIS_KEYS_ROLE.append("Team")
SYNTHESIS_KEYS_ROLE.append("Role")

SYNTHESIS_KEYS_WEIGHTED=SYNTHESIS_KEYS_ROLE
SYNTHESIS_KEYS_WEIGHTED.append("MedianFantasyEvaluation")
SYNTHESIS_KEYS_WEIGHTED.append("WeightedFantasyEvaluation")


SYNTHESIS_KEYS_RECENT=SYNTHESIS_KEYS_WEIGHTED
SYNTHESIS_KEYS_RECENT.append("Qt..A")
SYNTHESIS_KEYS_RECENT.append("Qt..I")
SYNTHESIS_KEYS_RECENT.append("Plays2018_2019")


BID_HEADERS=SYNTHESIS_KEYS_RECENT
BID_HEADERS.append("Owner")
BID_HEADERS.append("Price")
BID_HEADERS.append("MantraRole")



BONUS_GOAL=3
MALUS_GOAL=-1
BONUS_ASSIST=1
SCORED_PENALTY_BONUS=3
SAVED_PENALTY_BONUS=3
MISSED_PENALTY_MALUS=-3



def csv_from_excel(number_of_day):
    wb = xlrd.open_workbook(EXCEL_NAME+'.xlsx')
    sh = wb.sheet_by_name(SHEET_NAME)
    your_csv_file = open(CSV_NAME+str(number_of_day)+'.csv', 'w', encoding='utf8')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL, lineterminator='\n')

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

def clean_csv(day):
    searchfile=open(CSV_NAME+str(day)+'.csv')
    your_csv_file = open(CSV_NAME+str(day)+'final.csv', 'a')
    print(HEADERS,file=your_csv_file)
    for line in searchfile:
        if(line[1]>='0' and line[1]<='9'):
            print(line.rstrip()+',"'+str(day)+'"',file=your_csv_file)        
    searchfile.close()
    your_csv_file.close()
    os.remove(CSV_NAME+str(day)+'.csv')

def merge_csv():
    your_csv_file = open(TMP_DATASET_NAME, 'w')
    print(HEADERS,file=your_csv_file)
    for day in range(1,39):
        searchfile=open(CSV_NAME+str(day)+'final.csv')
        first=1
        for line in searchfile:
            if first==1:
                first=0
            else:
                print(line,file=your_csv_file,end="")


#this fucntion creates a file containing all days in range
def append_new_days(min_day_included,max_day_included,year):
    with open(FULL_DATASET_NAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(SINGLE_EVALUATION_KEYS)
        for day in range(min_day_included,max_day_included+1):
           
            with open(CSV_NAME+str(day)+'final.csv') as searchfile:
                reader=csv.reader(searchfile)
                first=True
                for row in reader:
                    if first:
                        first=False
                    else:
                        row.append("2018-19")
                        writer.writerow(row)



def assign_fantasy_evaluation():
    with open(FULL_DATASET_NAME,'r') as csvinput:
        print("Opening file      "+FULL_DATASET_NAME)
        with open(TMP_DATASET_NAME, 'w') as csvoutput:
            keys=SINGLE_EVALUATION_KEYS
            writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)

            reader = csv.DictReader(csvinput)

            all= []
            row={}
            for key in keys:
                row[key]=key
            all.append(row)

            for row in reader:
                row["Voto"]=row["Voto"].strip("*")
                fantasy_evaluation=float(row["Voto"])+BONUS_GOAL*float(row['Gf'])+MALUS_GOAL*float(row['Gs'])+BONUS_ASSIST*float(row['Ass'])
                fantasy_evaluation+=SAVED_PENALTY_BONUS*float(row["Rp"])
                fantasy_evaluation+=MISSED_PENALTY_MALUS*float(row["Rs"])
                fantasy_evaluation+=SCORED_PENALTY_BONUS*float(row["Rf"])
                row["FantasyEvaluation"]=fantasy_evaluation
                all.append(row)

            writer.writerows(all)

    os.remove(FULL_DATASET_NAME)
    os.rename(TMP_DATASET_NAME,FULL_DATASET_NAME)

def add_new_days_to_old():
    with open(FULL_DATASET_NAME,'r') as new_days_file:
        with open(DAYS, 'r') as old_days_file:
            
            reader_new = csv.DictReader(new_days_file)
            reader_old=csv.DictReader(old_days_file)
            all=[]
            row={}
            keys=SINGLE_EVALUATION_KEYS
            for key in keys:
                row[key]=key
            all.append(row)

            max=0
            for row in reader_old:
                all.append(row)
                if float(row["Day"])>max and row["Year"]=="2018-19":
                    max=float(row["Day"])
            first=True
            for row in reader_new:
                if first:
                    first=False
                elif float(row["Day"])>max:
                    all.append(row)
            with open(TMP_DATASET_NAME, 'w') as csvoutput:
                writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)
                writer.writerows(all)



def download():
#https://www.fantagazzetta.com/Servizi/Excel.ashx?type=1&g=6&t=275842789890&s=2018-19
    for day in range(6,7):

#https://www.fantagazzetta.com/Servizi/Excel.ashx?type=1&g=6&t=-4&s=2016-17

   # https://www.fantagazzetta.com/Servizi/Excel.ashx?type=1&g=2&t=275507133750&s=2018-19
        urllib.request.urlretrieve ("https://www.fantagazzetta.com/Servizi/Excel.ashx?type=1&g="+str(day)+"&t=275842789890&s=2018-19", EXCEL_NAME+".xlsx")
        csv_from_excel(day)
        os.remove(EXCEL_NAME+'.xlsx')
        clean_csv(day)


#C:/Users/asus/Desktop/Poli/fantasy-football/dataset/played_matches.csv


def concat_files():
    with open(FULL_DATASET_NAME,'r') as new_days_file:
        with open(DAYS, 'r') as old_days_file:
            
            reader_new = csv.DictReader(new_days_file)
            reader_old=csv.DictReader(old_days_file)

            all=[]
            row={}
            keys=SINGLE_EVALUATION_KEYS
            for key in keys:
                row[key]=key
            all.append(row)

            for row in reader_old:
                all.append(row)
            for row in reader_new:
                all.append(row)

            with open(TMP_DATASET_NAME, 'w') as csvoutput:
                writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)
                writer.writerows(all)

def main():
    download()
    #merge_csv()
    append_new_days(6,6,"2018-19")
    assign_fantasy_evaluation()
    add_new_days_to_old()
    #concat_files()
    pass
if __name__ == "__main__":
    main()
   