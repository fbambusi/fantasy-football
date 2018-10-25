from bs4 import BeautifulSoup
import urllib.request
from show_precise_roles import *

def download_html():
	try:
		html=urllib.request.urlopen ("https://www.fantagazzetta.com/probabili-formazioni-serie-a").read()
		print("Server Online")
		with open(LIKELY_FORMATIONS,"w") as formations_file:
		
			formations_file.write(str(html))
	except urllib.error.HTTPError as e:
		print("Server Offline")
		#do stuff here
	except urllib.error.URLError as e:
		print("Server Offline")
	 #do stuff here
	


def retrieve_players_html():
	with open(LIKELY_FORMATIONS,"r") as formations_file:
		return formations_file.read()


def probability_of_being_in_first_team(player_name,parsed_html):
	for a in parsed_html.find_all('a'):
		if player_name in a.contents:
			try:
				parent=a.parent.parent
				parent=parent.contents[1]
				parent=parent.contents[0]
				parent=parent.contents[0] #90%
				
				percentage=parent.contents[0]
				return (float(percentage.strip("%")))
			except AttributeError:
				return 0
	return 0

def first_team(players):
	html=str(retrieve_players_html())
	parsed_html = BeautifulSoup(html, 'html.parser')
	all=[]
	for player in players:
		probability=probability_of_being_in_first_team(player["Name"],parsed_html)
		player["Prob"]=probability
		player["Value"]=probability*float(player["MeanFantasyEvaluation"])
		#player["Value"]=player["WeightedFantasyEvaluation"]
		player["Value"]=player["MeanFantasyEvaluation"]
		if probability>30:
			all.append(player)

	return sorted(all,key=lambda p:p["Prob"],reverse=True)
	

#this function retrieves the players who are most likely to play and puts them in the most suitable position
def my_formation(players):
	
	my_players=first_team(players)
	slots=[]
	slots.append(Slot(["A","W"],2))
	slots.append(Slot(["A","Pc"],1))
	slots.append(Slot(["E"],2))
	slots.append(Slot(["M","C"],2))
	slots.append(Slot(["Dc"],3))
	slots.append(Slot(["Por"],1))



	slots=[]
	slots.append(Slot(["A","W"],2))
	slots.append(Slot(["A","Pc"],1))
	slots.append(Slot(["M"],1))
	slots.append(Slot(["M","C"],2))
	slots.append(Slot(["Dc"],2))
	slots.append(Slot(["Ds"],1))
	slots.append(Slot(["Dd"],1))
	slots.append(Slot(["Por"],1))


	my343=MantraSelection(slots)
	my343.fill(my_players)

	flow=GraphBlueprint(my343,my_players)
	all={}
	for player in flow.roles:
	    for role in flow.roles[player]:
	        if flow.roles[player][role]>0 and role!="sink" and role!="source" and player!="source" and player!="sink":
	            all[player]=role
	return all 

def my_formation_obj(player_list,player_dict):
	my_f=my_formation(player_list)
	all=[]
	for player in my_f:
		all.append(player_dict[player])
	return all

def main():
	download_html()
	players=my_players()
	player_dict={}
	for player in players:
		player_dict[player["Name"]]=player
	roles=my_formation(players)
	holders=[]
	bench=[]

	my_team=open("opponents/me1.txt","w")
	value=0
	for player in roles.keys():
		player_dict[player]["Where"]=roles[player]
		holders.append(player_dict[player])
		value=value+float(player_dict[player]["Value"])
	print("Value of team: "+str(value))
	for player in players:
		if player["Name"] not in roles:
			bench.append(player)
	print("YEEE")
	names=[]
	for player in holders:
		print(player["Name"]+"    "+str(player["Value"])+"     "+player["Where"]+"    "+player["Role"])
		my_team.write(player["Name"]+"\n")
	print("NOOOO=======================================================")
	roles=["P","D","C","A"]

	bench=sorted(bench,key=lambda p:p["Value"],reverse=True)
	
	for role in roles:
		print(role+"                <-------")
		for player in bench:
			#for role in player["MantraRole"]:
				if(player["Role"]==role):
					print(player["Name"]+"    "+str(player["Value"])+"    "+player["Role"]+"    "+role+"    "+str(player["Prob"]))
if __name__ == "__main__":
    main()