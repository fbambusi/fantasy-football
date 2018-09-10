from bs4 import BeautifulSoup
import urllib.request
from show_precise_roles import *

def download_html():
	return urllib.request.urlopen ("https://www.fantagazzetta.com/probabili-formazioni-serie-a").read()


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
	html=str(download_html())
	parsed_html = BeautifulSoup(html, 'html.parser')
	all=[]
	for player in players:
		probability=probability_of_being_in_first_team(player["Name"],parsed_html)
		player["Prob"]=probability
		if probability>5:
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

	my343=MantraSelection(slots)
	my343.fill(my_players)

	flow=GraphBlueprint(my343,my_players)
	all={}
	for player in flow.roles:
	    for role in flow.roles[player]:
	        if flow.roles[player][role]>0 and role!="sink" and role!="source" and player!="source" and player!="sink":
	            all[player]=role
	return all 

def main():
	players=my_players()
	player_dict={}
	for player in players:
		player_dict[player["Name"]]=player
	roles=my_formation(players)
	holders=[]
	bench=[]

	for player in roles.keys():
		player_dict[player]["Where"]=roles[player]
		holders.append(player_dict[player])
	for player in players:
		if player["Name"] not in roles:
			bench.append(player)
	print("YEEE")
	for player in holders:
		print(player["Name"]+"    "+str(player["WeightedFantasyEvaluation"])+"     "+player["Where"])
	print("NOOOO")
	for player in bench:
		print(player["Name"]+"    "+str(player["WeightedFantasyEvaluation"]))
if __name__ == "__main__":
    main()