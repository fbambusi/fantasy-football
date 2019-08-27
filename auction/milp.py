import random
from functools import reduce
import matplotlib.pyplot as plt
import subprocess
import time
from amplpy import AMPL,Environment
import numpy as np


#start 10:10 end 10:18

ampl = AMPL(Environment('/home/asino/Downloads/ampl_linux-intel64/'))
ampl.setOption("solver","/home/asino/Downloads/ampl_linux-intel64/cplex")
random.seed(7)
np.random.seed(7)
players={}
playersList= []
bidders = {}
biddersList = []
NBIDDERS = 8
BUDGET = 500
INCREMENT=1


PLAYERS_PER_ROLE = {"A":30,"C":50,"D":50,"P":20}
VAR_PER_ROLE={"A":5,"C":3,"D":2,"P":1}

for role,number in PLAYERS_PER_ROLE.items():
	for i in range(number):
		player = {}
		player["name"] = role+str(i)
		player["perf"] = np.random.normal(scale=VAR_PER_ROLE[role])#random.random()
		player["cost"] = 1
		if player["perf"]>player["cost"]:
			player["cost"]=player["perf"] * 10
		player["role"] = role
		player["bought"]= 0
		playersList.append(player)
		players[player["name"]]=player


for i in range(NBIDDERS):
	bidder={}
	bidder["name"]=i
	bidder["players"]=[]
	bidder["money"]=BUDGET
	bidders[bidder["name"]]= bidder
	biddersList.append(bidder)


#currG=0


def initializeMilp(players,playersList):
	
	roleCompatibilityString = "set CompatibilityPlayerRole:= \n"
	performanceString = "param:performance := \n"
	costString = "param :cost:= \n"
	playersString = "set Players:= "
	boughtParameterString= "param:alreadyBought:="
	cont=0

	for player in playersList:
		if not player["bought"]:
			cont+=1
			roleCompatibilityString+= "({},*) {}\n".format(player["name"],player["role"])
			performanceString+= "{} {}\n".format(player["name"],player["perf"])
			costString+= "{} {}\n".format(player["name"],player["cost"])
			boughtParameterString+= "{} {}\n".format(player["name"],player["bought"])
			playersString+= " {} ".format(player["name"])

	print("{} players available".format(cont))



	roleCompatibilityString+= ";\n"
	performanceString+= ";\n"
	costString+= ";\n"
	playersString+= ";\n"
	boughtParameterString+= ";\n"
	with open('dat-file-configuration.txt', 'r') as file:
	    fixedHeader  =  file.read()
	    with open('fantasy-auction.dat', 'w') as outputFile:
	    	outputFile.write("param  budget:={};\n".format(BUDGET))
	    	outputFile.write(fixedHeader)
	    	outputFile.write(playersString)
	    	outputFile.write(roleCompatibilityString)
	    	outputFile.write(performanceString)
	    	outputFile.write(costString)
	    	outputFile.write(boughtParameterString)

	ampl.read("fantasy-auction.mod")

	ampl.readData("fantasy-auction.dat")

	
	
	
				
	

def parseMilpSolution(playersList):
	ampl.solve()
	buy=ampl.getVariable("buy")

	solution=buy.getValues().toDict()
	
	
	idx = 0
	boughtPlayers=[]
	for player in playersList:
		if solution[player["name"]]==1:
			player["bought"]=1
			boughtPlayers.append(player)

	return boughtPlayers

def updateMilp(players,boughtPlayers):
	alreadyBought=ampl.getParameter("alreadyBought")
	dictOfNewValues={}
	for name,player in players.items():
		dictOfNewValues[name]=player["bought"]
	alreadyBought.setValues(dictOfNewValues)


def updateAtEndOfRound(acquisitionList,roundNumber):
	costParam=ampl.getParameter("cost")
	dictOfNewValues={}
	bidderIndex=0
	for entry in acquisitionList:
		for player in entry:
			player["cost"]+=INCREMENT*(NBIDDERS-bidderIndex)
			dictOfNewValues[player["name"]]=player["cost"]
		bidderIndex+=1
	costParam.setValues(dictOfNewValues)


	alreadyBought=ampl.getParameter("alreadyBought")
	dictOfNewValues={}
	for name,player in players.items():
		player["bought"]=0
		dictOfNewValues[name]=player["bought"]
	alreadyBought.setValues(dictOfNewValues)

	pass

initializeMilp(players,playersList)
countBid=0
histories=[]
nAcquisitions=[]
for i in range(15):
	print("New round\n")
	acquisitionList=[]
	currRound=[]
	for name,bidder in bidders.items():
		pls=parseMilpSolution(playersList)
		updateMilp(players,pls)

		acquisitionList.append(pls)
		value=reduce(lambda x,y:x+y,map(lambda pippo:pippo["perf"],pls))
		currRound.append(value)

		print(value)
		#time.sleep(2)
	nAcquisitions.append(len(pls))
	histories.append(currRound)
	updateAtEndOfRound(acquisitionList,i)
	print("{} players bought".format(len(pls)))

perfs=[]
costs=[]
for player in playersList:
	perfs.append(player["perf"])
	costs.append(player["cost"])
#plt.plot(histories)
plt.scatter(perfs,costs)

plt.show()

plt.plot(nAcquisitions)

#plt.hist(perfs)

plt.show()