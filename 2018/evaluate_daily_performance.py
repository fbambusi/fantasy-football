from show_precise_roles import *

def get_recent_players():
	your_csv_file = open("dataset/Quotazioni_Fantacalcio_Ruoli_Mantra.csv", 'r')
	return csv.DictReader(your_csv_file)

def get_days():
	your_csv_file = open(DAYS, 'r')
	return csv.DictReader(your_csv_file)
	
def main():
	players_list=get_players()
	players={}
	
	recent=[]
	recent_p=get_recent_players()
	for player in recent_p:
		recent.append(player["Name"])

	for player in players_list:
		players[player["Name"]]=player["WeightedFantasyEvaluation"]
	
	keys=DAILY_KEYS
	all=[]
	days=get_days()
	row={}
	for key in keys:
	    row[key]=key
	all.append(row)

	for day in days:
		try:
			day["Delta"]=float(day["FantasyEvaluation"])-float(players[day["Nome"]])
			all.append(day)
		except KeyError:
			if day["Nome"] in recent:
				print(day["Nome"]+"  not found")
		

	
	csvoutput=open(TMP_DATASET_NAME,"w")

	writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)
	writer.writerows(all)

if __name__ == "__main__":
    main()
