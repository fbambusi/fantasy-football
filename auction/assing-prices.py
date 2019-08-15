import random
from functools import reduce
import matplotlib.pyplot as plt

random.seed(7)
players=[]
bidders={}
biddersList=[]
NPLAYERS=4
NBIDDERS=7
BUDGET=500
INCREMENT=5

OVERALL_PLAYERS=300

PERF_DECREASE=0.25

def generatePlayers():
	for i in range(OVERALL_PLAYERS):
		player={}
		player["perf"]=random.random()
		player["perf"]**=4
		player["price"]=1
		player["owner"]="MARKET"
		players.append(player)

	players=sorted(players,key=lambda pippo:pippo["perf"])
	return players
players=generatePlayers()

for i in range(NBIDDERS):
	bidder={}
	bidder["name"]=i
	bidder["players"]=[]
	bidder["money"]=BUDGET
	bidders[bidder["name"]]= bidder
	biddersList.append(bidder)

counter=0
for i in range(NPLAYERS*NBIDDERS):
	biddersList[i%NBIDDERS]["players"].append(players[counter])
	players[counter]["owner"]=biddersList[i%NBIDDERS]["name"]
	counter+=1


for bidd in bidders:
	print(bidders[bidd]["players"])
	print()


def sell(bidder,playerToSell):
	bidder["money"]+=playerToSell["price"]
	bidder["players"].remove(playerToSell)
	playerToSell["owner"]="MARKET"

def buy(bidder,playerToBuy):
	
	if bidder["money"]>=playerToBuy["price"]:
		bidder["money"]-=playerToBuy["price"]
		bidder["players"].append(playerToBuy)
		playerToBuy["owner"]=bidder["name"]
		return 0
	return 1

def acquire(bidder,playerToBuy):
	bidder["money"]=0
	playerToBuy["owner"]=bidder["name"]
	bidder["players"].append(playerToBuy)

trans=0
for i in range(400000):
	for bidder in biddersList:
		
		playerToSwap=random.choice(bidder["players"])
		sell(bidder,playerToSwap)
		playerToSwap["price"]+=INCREMENT
		ok=False
		
		existsAffordablePlayer=False
		for player in players:
			if player["owner"]=="MARKET" and player["price"]<=bidder["money"]:
				existsAffordablePlayer=True
		if not existsAffordablePlayer:
			print("Too poor to buy")
			acquire(bidder,playerToSwap)
			break
		threshold=playerToSwap["perf"]+3*PERF_DECREASE*random.random()
		while 1 :
			
			
			for player in players:
				if player["perf"]>threshold and player["owner"]=="MARKET":
					if not buy(bidder,player):
						ok=True
						trans+=1
						break
			if ok:
				#print("Transaction ok")
				break		
			threshold-=PERF_DECREASE
			
	if not ok:
		break
for bidder in biddersList:
	perf =  reduce((lambda x, y: x + y), map(lambda pl:pl["perf"],bidder["players"]))
	print(perf)
	print(bidder["money"])

print(players)

print(trans)
plt.scatter(list(map(lambda p:p["perf"],players)),list(map(lambda p:p["price"],players)))
plt.show()				
