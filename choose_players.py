from operator import itemgetter
from download_dataset import *
import csv


class Selection:
	def __init__(self,defenders,midfielders,attackers):
		self.max={}
		self.max["D"]=defenders
		self.max["C"]=midfielders
		self.max["A"]=attackers
		self.max["P"]=1
		self.max["COACH"]=0
		self.players={"A":[],"C":[],"D":[],"COACH":[],"P":[]}

	def add_player(self,players):
		cont=0
		while len(self.players[players[cont]["Role"]])>=self.max[players[cont]["Role"]]:
			cont=cont+1
		self.players[players[cont]["Role"]].append(players[cont])
		return players[cont+1:]

def  get_players():
	attackers_file=open(PLAYER_SYNTHESIS)
	return (csv.DictReader(attackers_file))

def filter_by_role(all_players,role):
	return filter(lambda x:x["Role"]==role,all_players)



selection= Selection(4,4,2)

players=get_players()
attackers=filter_by_role(players,"A")
defenders=filter_by_role(players,"D")
midfielders=filter_by_role(players,"M")

players = sorted(players, key=itemgetter('WeightedFantasyEvaluation'),reverse=True) 


for i in range(1,12):
	players=selection.add_player(players)

for zone in selection.players:
	for attacker in selection.players[zone]:
		print(attacker["Name"]+"   "+attacker["WeightedFantasyEvaluation"]+"   "+ attacker["Role"])

