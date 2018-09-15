from show_precise_roles import *

def evaluate(filename):
	file_=open("opponents/"+filename,"r")
	data=file_.readlines()
	players=get_players_dict()
	value=0
	for player_name in data:
		value=value+float(players[player_name.strip()]["MeanFantasyEvaluation"])
	return value


evaluate("gatti1.txt")