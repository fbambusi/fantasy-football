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
		
		self.players={"A":[],"C":[],"D":[],"P":[]}

	def add_player(self,players):
		cont=0
		while len(self.players[players[cont]["Role"]])>=self.max[players[cont]["Role"]]:
			cont=cont+1
		self.players[players[cont]["Role"]].append(players[cont])
		return players[cont+1:]

	def add_player_object(self,player):
		self.players[player["Role"]].append(player)
		self.players[player["Role"]]=sorted(self.players[player["Role"]],key=lambda x:x["WeightedFantasyEvaluation"])
		print("Adding "+player["Name"])

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

	def value_of_zone(self,zone):
		value=0
		for player in self.players[role]:
				value=value+self.probability_to_play(role,pos)*float(player["WeightedFantasyEvaluation"])
				pos=pos+1
		return value
	def avg_value_zone(self,zone):
		value=0
		pos=0
		for player in self.players[zone]:
				value=value+self.probability_to_play(zone,pos)*float(player["WeightedFantasyEvaluation"])
				pos=pos+1
		if len(self.players[zone])>0:
			return value/len(self.players[zone])
		else:
			return 0

	def fill(self,players):
	
		self.show_players()
		self.clear_not_fixed()
		
		number_of_players=0
		players_copy=copy.copy(players)
		for role in self.max.values():
			number_of_players=number_of_players+role
		for role in self.players.keys():
			number_of_players=number_of_players-len(self.players[role])
		for i in range(1,number_of_players+1):
			best=self.add_best_player(players_copy)
			players_copy.remove(best)
		for role in self.players.keys():
			self.players[role]=sorted(self.players[role],key=lambda x:x["WeightedFantasyEvaluation"],reverse=True)

	def clear_not_fixed(self):
		for role in self.max.keys():
			tmp=[]
			for player in self.players[role]:
				if player["Owner"]=="ME":
					tmp.append(player)
			self.players[role]=tmp

	def module(self):
		return str(self.normal["D"])+" "+str(self.normal["C"])+" "+str(self.normal["A"])

	def show_players(self):
		for zone in self.players:
			for attacker in self.players[zone]:
				print(attacker["Name"]+"   "+attacker["WeightedFantasyEvaluation"]+"   "+ attacker["Role"]+ "  "+attacker["Owner"])

class Competitor:
	def __init__(self,name,selection,budget):
		self.budget=budget
		self.selection=selection
		self.name=name
		self.prices={"A":0,"D":0,"C":0,"P":0}

	def  buy(self,player,cost):
		self.budget=self.budget-cost
		self.selection.add_player_object(player)
		self.prices[player["Role"]]=self.prices[player["Role"]]+cost
	def show(self):
		print("Competitor: "+self.name)
		print("Money: "+str(self.budget))
		for zone in self.selection.players.keys():
			print("Zone: "+zone)
			print("Cost: "+str(self.prices[zone]))
			print("Avg value: "+str(self.selection.avg_value_zone(zone)))



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

def get_by_surname(players,surname):
	for item in players:
		if item["Name"]==surname:
			return item
	print("PLAYER NOT FOUND   "+surname )



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

	return modules

def fill(modules,players):
	for pnt in modules:
		pnt.fill(players)

	modules=sorted(modules,key=lambda p:p.get_value(),reverse=True)
	for pnt in modules:
		print(pnt.module()+" "+ str(pnt.get_value()))

	modules[0].show_players()
	return modules

def store(players,version):
	csvoutput=open("dataset/bid/version"+str(version)+".csv", 'w')
	keys=BID_HEADERS
	writer = csv.DictWriter(csvoutput, quoting=csv.QUOTE_ALL, lineterminator='\n',fieldnames=keys)
	all=[]
	row={}
	for key in keys:
	    row[key]=key
	all.append(row)
	for player in players:
		all.append(player)
	writer.writerows(all)
	csvoutput.close()

players=get_players()

players = sorted(players, key=itemgetter('WeightedFantasyEvaluation'),reverse=True) 



fake_sel=Selection(8,8,8)
competitors={}
competitors["BRYAN"]=Competitor("BRYAN",copy.deepcopy(fake_sel),500)
competitors["GATTI"]=Competitor("GATTI",copy.deepcopy(fake_sel),500)
competitors["VE"]=Competitor("VE",copy.deepcopy(fake_sel),500)


modules=init()
modules=fill(modules,players)

all=[]
for player in players:
	if float(player["Plays2018_2019"])==1 and (player["Owner"]==None or player["Owner"]==""):
		all.append(player)
	
	if player["Owner"]!=None and player["Owner"]!="ME" and player["Owner"]!="":
		competitors[player["Owner"]].buy(player,float(player["Price"]))

	if player["Owner"]=="ME":
		for module in modules:
			module.add_player_object(player)


players=copy.copy(all)

#===========================================================================================
#=========================================MAIN==============================================
#===========================================================================================
command=""
counter=0
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
	if command=="buy" or command=="b":
		print("Owner:")
		owner=sys.stdin.readline()
		owner=owner.strip()
		owner=owner.upper()
		print("Player:")
		player=sys.stdin.readline()
		player=player.strip()
		player=player.upper()
		print("Price:")
		price=sys.stdin.readline()
		price=price.strip()
		price=price.upper()
		player_obj=get_by_surname(players,player)
		competitors[owner].buy(player_obj,float(price))
		remove_by_surname(players,player)
		player_obj["Price"]=price
		player_obj["Owner"]=owner
		competitors[owner].show()

	if command=="display" or command=="d":
		print("Owner:")
		owner=sys.stdin.readline()
		owner=owner.strip()
		owner=owner.upper()
		competitors[owner].show()
	if command=="compute" or command=="c":
		modules=fill(modules,players)
	if command=="store" or command=="s":
		store(all,counter)
		counter=counter+1
	if command=="me" or command=="m":
		print("Who I bought:")
		owner=sys.stdin.readline()
		owner=owner.strip()
		owner=owner.upper()
		player_obj=get_by_surname(players,owner)
		print(player_obj["Name"])
		player_obj["Owner"]="ME"
		for module in modules:
			module.add_player_object(player_obj)
	