from operator import itemgetter
from download_dataset import *
from functools import reduce
import csv
from scipy.stats import binom
import numpy
import copy
import sys
class Selection:

	def __init__(self,defenders,midfielders,attackers):
		self.normal={}
		self.normal["D"]=defenders
		self.normal["C"]=midfielders
		self.normal["A"]=attackers
		self.normal["P"]=1
		self.max={}
		self.max["D"]=8
		self.max["C"]=8
		self.max["A"]=8
		self.max["P"]=3
		#self.max["COACH"]=0
		
		self.players={"A":[],"C":[],"D":[],"COACH":[],"P":[]}

	def add_player(self,players):
		cont=0
		while len(self.players[players[cont]["Role"]])>=self.max[players[cont]["Role"]]:
			cont=cont+1
		self.players[players[cont]["Role"]].append(players[cont])
		return players[cont+1:]


	#Positions start at 0
	def probability_to_play(self,role,position):
		if position<self.normal[role]:
			return 1
		else:
			needed_failures=position-self.normal[role]
			vett= list(map(lambda w:float(w["PlayedMatches"])/38, self.players[role][:position]))
			average_success_probability=numpy.mean(vett)
			tot_prob=1-binom.cdf(needed_failures,position,1-average_success_probability)
			return tot_prob

	def add_best_player(self,players):
		tmp_best_player={}
		tmp_best_score=-10
		tmp_role=""
		for role in self.max.keys():
			curr_player=best_player_by_role(players,role)
			print(curr_player)
			curr_probability_to_play=self.probability_to_play(role,len(self.players[role]))
			curr_score=curr_probability_to_play*float(curr_player["WeightedFantasyEvaluation"])

			if curr_score>tmp_best_score and len(self.players[role])<self.max[role]:
				tmp_best_score=curr_score
				tmp_best_player=curr_player
				tmp_role=role
		self.players[tmp_role].append(tmp_best_player)
		return tmp_best_player
	
	def get_value(self):
		value=0
		for role in self.max.keys():
			pos=0
			for player in self.players[role]:
				value=value+self.probability_to_play(role,pos)*float(player["WeightedFantasyEvaluation"])
				pos=pos+1
		return value

	def fill(self,players):
		number_of_players=0
		players_copy=copy.copy(players)
		for role in self.max.values():
			number_of_players=number_of_players+role
		for i in range(1,number_of_players+1):
			best=self.add_best_player(players_copy)
			players_copy.remove(best)

	def module(self):
		return str(self.normal["D"])+" "+str(self.normal["C"])+" "+str(self.normal["A"])

	def show_players(self):
		for zone in self.players:
			for attacker in self.players[zone]:
				print(attacker["Name"]+"   "+attacker["WeightedFantasyEvaluation"]+"   "+ attacker["Role"])

def  get_players():
	attackers_file=open(PLAYER_SYNTHESIS)
	return (csv.DictReader(attackers_file))

def filter_by_role(all_players,role):
	return filter(lambda x:x["Role"]==role,all_players)

def best_player_by_role(players,role):
	for player in players:
		if player["Role"]==role:
			return player
	print("NNNNOOOOOO"+role)

def remove_by_surname(players,surname):
	for item in players:
		if item["Name"]==surname:
			players.remove(item)






def init():
	modules=[]
	selection= Selection(4,4,2)

	modules.append(selection)

	selection2=Selection(4,3,3)
	modules.append(selection2)

	selection3=Selection(3,5,2)
	modules.append(selection3)


	selection4=Selection(3,4,3)
	modules.append(selection4)


	selection5=Selection(4,5,1)
	modules.append(selection5)

	selection6=Selection(5,3,2)
	modules.append(selection6)


	selection7=Selection(5,4,1)
	modules.append(selection7)

	selection8=Selection(6,3,1)
	modules.append(selection8)

	selection9=Selection(3,6,1)
	modules.append(selection9)


	for pnt in modules:
		pnt.fill(players)

	modules=sorted(modules,key=lambda p:p.get_value(),reverse=True)
	for pnt in modules:
		print(pnt.module()+" "+ str(pnt.get_value()))

	modules[0].show_players()
	return modules

players=get_players()

players = sorted(players, key=itemgetter('WeightedFantasyEvaluation'),reverse=True) 

all=[]
for player in players:
	if float(player["Plays2018_2019"])==1:
		all.append(player)
		
players=all
print(len(players))
command=""
print("Scrivi qlcs")
while command!= "q":
	command=sys.stdin.readline()
	command=command.strip()
	if command=="remove" or command=="r":
		print("Player:")
		who=sys.stdin.readline()
		who=who.strip()
		who=who.upper()
		print(who)
		remove_by_surname(players,who)
		init()




