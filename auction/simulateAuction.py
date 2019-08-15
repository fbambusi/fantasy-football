import random

from bidder import bidder
from player import traditionalPlayer

NBIDDERS=7
BUDGET=500
NPLAYERS=100

LEARNING_RATE=0.1

players=[]
random.seed(19)

for i in range(NPLAYERS):
	players.append(traditionalPlayer(i,random.random(),"A"))
players=sorted(players,key=lambda p:p.getPerformance())
bidders=[]

for i in range(NBIDDERS):
	bid=bidder()
	bid.setBudget(BUDGET)
	bid.randomizeEvaluation(players)
	bidders.append(bid)


def getBuyerAndPrice(bidders,desiredPlayer):
	dest=False
	price=0
	for bidder in bidders:
		if not dest:
			dest=bidder
			vls=bidder.getValueOfPlayers()
			price=vls[desiredPlayer.getName()]
		else:
			pls=bidder.getDesiredPlayers(players)
			if desiredPlayer in pls:
				vls=bidder.getValueOfPlayers()
				if vls[desiredPlayer.getName()]>price:
					dest=bidder
					price=price+1
	return dest,price
	

pls=list(players)

deltas=[]
perfs={}
for bid in bidders:
	perfs[bid]=[]

for j in range(800):
	players=pls
	pls=list(players)
	for i in range(10):
		for currentBidder in bidders:
			desiredPlayer=currentBidder.getDesiredPlayers(players)[0]
			buyer,price=getBuyerAndPrice(bidders,desiredPlayer)
			buyer.buyPlayer(desiredPlayer,price)
			print(buyer,price)
			players.remove(desiredPlayer)
			print(desiredPlayer.getName())

	bidders=sorted(bidders, key=lambda p:p.getPerformanceOfTeam())
	print("\n\n")	
	deltas.append(bidders[0].getPerformanceOfTeam()-bidders[-1].getPerformanceOfTeam())

	for bidder in bidders[:-1]:
		print(bidder.getPerformanceOfTeam())

		bidder.correctValueOfPlayers(bidders[-1],LEARNING_RATE)

	bidders[-1].randomlyCorrectValueOfPlayers(LEARNING_RATE)

	for bid in bidders:
		perfs[bid].append(bid.getPerformanceOfTeam())
		bid.resetOwnedPlayers()

import matplotlib.pyplot as plt

for pf in perfs.keys():
	pass
	#plt.plot(perfs[pf])
plt.plot(deltas)
plt.show()