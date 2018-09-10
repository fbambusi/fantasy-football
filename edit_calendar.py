from download_dataset import *
import copy
def matche():
	file1=open("dataset/calendario-serie-A-2017-2018-refined.csv","r")
	return csv.DictReader(file1)



def maino():
	matches=matche()
	days=[]
	for match in matches:
		teams=match["Match"].split("-")
		row={}
		row["Team1"]=teams[0]
		row["Team2"]=teams[1]
		days.append(row)
		row2={}
		row2["Team1"]=teams[1]
		row2["Team2"]=teams[0]
		days.append(row2)
	days2=days
	for day in days:
		row={}
		row["Team1"]=day["Team1"]
		row["Team2"]=day["Team2"]
		days2.append(row)
	cont=0
	for day in days2:
		day["Day"]=cont//20
		cont=cont+1	
	keys=["Team1","Team2","Day"]
	csvoutput=open("dataset/calendar2017-2018.csv","w")
	writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)
	writer.writerows(days)



maino()