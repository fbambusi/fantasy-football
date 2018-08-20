import urllib.request
import xlrd
import csv
import os
import csv

EXCEL_NAME="dataset/day"
CSV_NAME="dataset/day"
FULL_DATASET_NAME="dataset/all_days.csv"
TMP_DATASET_NAME="dataset/all_days_tmp.csv"
SHEET_NAME="Fantagazzetta"
HEADERS='"Cod.","Ruolo","Nome","Voto","Gf","Gs","Rp","Rs","Rf","Au","Amm","Esp","Ass","Asf","Gdv","Gdp","Day"'
SINGLE_EVALUATION_KEYS=["Cod.","Ruolo","Nome","Voto","Gf","Gs","Rp","Rs","Rf","Au","Amm","Esp","Ass","Asf","Gdv","Gdp","Day"]
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
    your_csv_file = open(FULL_DATASET_NAME, 'w')
    print(HEADERS,file=your_csv_file)
    for day in range(1,39):
        searchfile=open(CSV_NAME+str(day)+'final.csv')
        first=1
        for line in searchfile:
            if first==1:
                first=0
            else:
                print(line,file=your_csv_file,end="")

#for day in range(1,39):
#    urllib.request.urlretrieve ("https://www.fantagazzetta.com/Servizi/Excel.ashx?type=1&g="+str(day)+"&t=-4&s=2017-18", EXCEL_NAME+".xlsx")
#    csv_from_excel(day)
#    os.remove(EXCEL_NAME+'.xlsx')
#    clean_csv(day)


#C:/Users/asus/Desktop/Poli/fantasy-football/dataset/played_matches.csv
#merge_csv()
