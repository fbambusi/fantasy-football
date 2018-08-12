import urllib.request
import xlrd
import csv
import os
import csv

EXCEL_NAME="day"
CSV_NAME="day"
SHEET_NAME="Fantagazzetta"
HEADERS='"Cod.","Ruolo","Nome","Voto","Gf","Gs","Rp","Rs","Rf","Au","Amm","Esp","Ass","Asf","Gdv","Gdp","Day"'
def csv_from_excel(number_of_day):
    wb = xlrd.open_workbook(EXCEL_NAME+'.xlsx')
    sh = wb.sheet_by_name(SHEET_NAME)
    your_csv_file = open(CSV_NAME+'.csv', 'w', encoding='utf8')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

def clean_csv():
    searchfile=open(CSV_NAME+'.csv')
    your_csv_file = open(CSV_NAME+'final.csv', 'a')
    print(HEADERS,file=your_csv_file)
    for line in searchfile:
        if(line[1]>='0' and line[1]<='9'):
            print(line.rstrip()+',"2"',file=your_csv_file)        
    searchfile.close()

urllib.request.urlretrieve ("https://www.fantagazzetta.com/Servizi/Excel.ashx?type=1&g=2&t=-4&s=2017-18", EXCEL_NAME+".xlsx")
csv_from_excel(1)
os.remove(EXCEL_NAME+'.xlsx')
clean_csv()

