import random

from bidder import bidder
from player import traditionalPlayer

NBIDDERS=7
BUDGET=500
NPLAYERS=100

LEARNING_RATE=0.7

NEEDED_PLAYERS=11
players=[]

NROUNDS=6000*20
random.seed(19)

for i in range(NPLAYERS):
	players.append(traditionalPlayer(i,random.random()**5,"A"))
players=sorted(players,key=lambda p:-p.getPerformance())
bidders=[]

for i in range(NBIDDERS):
	bid=bidder(BUDGET)
	bid.setBudget(BUDGET)
	bid.randomizeEvaluation(players)
	bidders.append(bid)

def everyBidderHasFullTeam(bidders):
	for bidder in bidders:
		if bidder.getNumberOfOwnedPlayers()<NEEDED_PLAYERS:
			return False
	return True


def costFunction(bidders,players):
	players=pls
	pls=list(players)

	while not everyBidderHasFullTeam(bidders):
		for currentBidder in bidders:
			if currentBidder.getNumberOfOwnedPlayers()<NEEDED_PLAYERS:
				desiredPlayer=currentBidder.getDesiredPlayers(players)[0]
				buyer,price=getBuyerAndPrice(bidders,desiredPlayer)
				if buyer:
					buyer.buyPlayer(desiredPlayer,price)
							
					players.remove(desiredPlayer)
		
	bidders=sorted(bidders, key=lambda p:p.getPerformanceOfTeam())
	delta=bidders[0].getPerformanceOfTeam()-bidders[-1].getPerformanceOfTeam()

	return delta,bidders[-1]

def stepOfGradientDescent(bidders,players,playerToUpdate,winningBidder,signedIncrement):
	for bidder in bidders:
		if bidder != winningBidder:
			bidder.correctValueOfPlayers(bidders[-1],LEARNING_RATE)
	winningBidder.correctValueOfPlayer(playerToUpdate.getName(),signedIncrement)

def gradientDescent(bidders,players,playerToUpdate):
	initialValue,winner=costFunction(bidders,players)
	initialGradient=LEARNING_RATE
	costHistory=[]
	for i in range(100):
		stepOfGradientDescent(bidders,players,playerToUpdate,winner,initialGradient)
		newValue=costFunction(bidders,players)
		initialGradient=(newValue-initialValue)/(initialGradient)
		initialValue=newValue
		costHistory.append(newValue)

def getBuyerAndPrice(bidders,desiredPlayer):
	dest=False
	price=0
	
	bds=sorted(bidders,key=lambda b:-b.getValueOfPlayers()[desiredPlayer.getName()])
	oldBid=False
	oldVal=0
	for bid in bds:
		if oldBid:
			curVal=bid.getValueOfPlayers()[desiredPlayer.getName()]
			if oldBid.canPay(curVal) and oldBid.getNumberOfOwnedPlayers()<NEEDED_PLAYERS:
				return oldBid,curVal
		oldBid=bid

	for bidder in bidders:
		if bidder.getNumberOfOwnedPlayers()<=NEEDED_PLAYERS:
			if not dest:
				dest=bidder
				price=price+1
			else:
				pls=bidder.getDesiredPlayers(players)
				if desiredPlayer in pls:
					vls=bidder.getValueOfPlayers()
					if vls[desiredPlayer.getName()]>price:
						
						price2=dest.getValueOfPlayers()[desiredPlayer.getName()]+1
						if bidder.canPay(price2):
							dest=bidder
							price=price2
	return dest,price
	

pls=list(players)

deltas=[]
perfs={}
budgets={}
for bid in bidders:
	perfs[bid]=[]
	budgets[bid]=[]

for player in players:
	print(player.getPerformance())
print("\n\n")
print(bidders[0].getDesiredPlayers(players)[0].getPerformance())


for j in range(NROUNDS):
	if j%1000==0:
		print(j)
	players=pls
	pls=list(players)

	while not everyBidderHasFullTeam(bidders):
		for currentBidder in bidders:
			if currentBidder.getNumberOfOwnedPlayers()<NEEDED_PLAYERS:
				desiredPlayer=currentBidder.getDesiredPlayers(players)[0]
				buyer,price=getBuyerAndPrice(bidders,desiredPlayer)
				if buyer:
					buyer.buyPlayer(desiredPlayer,price)
							
					players.remove(desiredPlayer)
		
	bidders=sorted(bidders, key=lambda p:p.getPerformanceOfTeam())
	deltas.append(bidders[0].getPerformanceOfTeam()-bidders[-1].getPerformanceOfTeam())

	for bidder in bidders[:-1]:
	
		bidder.correctValueOfPlayers(bidders[-1],LEARNING_RATE)

	bidders[-1].randomlyCorrectValueOfPlayers(LEARNING_RATE,BUDGET)

	for bid in bidders:
		perfs[bid].append(bid.getPerformanceOfTeam())
		bid.resetOwnedPlayers()
		budgets[bid].append(bid.getBudget())
		bid.setBudget(BUDGET)

import matplotlib.pyplot as plt

'''
for pf in perfs.keys():
	pass
	#plt.plot(perfs[pf])
plt.plot(deltas)
plt.show()

for bid in bidders:
	plt.plot(perfs[bid])
	break

	
plt.show()
'''
for bid in bidders:
	vls=bid.getValueOfPlayers()

	px=[]
	py=[]
	for player in pls:
		px.append(player.getPerformance())
		py.append(vls[player.getName()])
	plt.plot(budgets[bid])
#	plt.scatter(px,py)

plt.show()
px=[]
py=[]

for player in pls:
	px.append(player.getPerformance())
	prs=[]
	for bidder in bidders:
		prs.append(bidder.getValueOfPlayers()[player.getName()])
	prs=sorted(prs)
	py.append(prs[-2])
plt.scatter(px,py)
plt.show()