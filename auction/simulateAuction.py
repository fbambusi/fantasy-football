import random

from bidder import bidder
from player import traditionalPlayer
import matplotlib.pyplot as plt


NBIDDERS=9
BUDGET=500
NPLAYERS=120

LEARNING_RATE=0.4

NEEDED_PLAYERS=11
players=[]

NROUNDS=6000*20
random.seed(19)

PATIENCE=20
def everyBidderHasFullTeam(bidders):
	for bidder in bidders:
		if bidder.getNumberOfOwnedPlayers()<NEEDED_PLAYERS:
			return False
	return True


def costFunction(bidders,players):
	while not everyBidderHasFullTeam(bidders):
		for currentBidder in bidders:
			if currentBidder.getNumberOfOwnedPlayers()<NEEDED_PLAYERS:
				desiredPlayer=currentBidder.getDesiredPlayers(players)[0]
				buyer,price=getBuyerAndPrice(bidders,desiredPlayer)
				if buyer:
					buyer.buyPlayer(desiredPlayer,price)
							
					players.remove(desiredPlayer)
		
	bidders=sorted(bidders, key=lambda p:p.getPerformanceOfTeam())
	delta=-bidders[0].getPerformanceOfTeam()+bidders[-1].getPerformanceOfTeam()

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
	evaluationHistory={}
	for bidder in bidders:
		evaluationHistory[bidder]=[]
	nStepsWithoutChange=0
	for i in range(800):
		stepOfGradientDescent(bidders,players,playerToUpdate,winner,initialGradient)
		newValue,winner=costFunction(bidders,players)
		initialValue=newValue
		costHistory.append(newValue)
		for bidd in bidders:
			evaluationHistory[bidd].append(bidd.getValueOfPlayers()[playerToUpdate.getName()])
		if initialGradient==0:
			nStepsWithoutChange+=1
			initialGradient=LEARNING_RATE*(-2)**nStepsWithoutChange
		else:
			nStepsWithoutChange=0
			initialGradient=(newValue-initialValue)/(initialGradient)
		
	return costHistory,evaluationHistory

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
	
def main():
	players=[]
	for i in range(NPLAYERS):
		players.append(traditionalPlayer(i,random.random()**5,"A"))
	players=sorted(players,key=lambda p:-p.getPerformance())
	bidders=[]

	for i in range(NBIDDERS):
		bid=bidder(BUDGET)
		bid.setBudget(BUDGET)
		bid.randomizeEvaluation(players)
		bidders.append(bid)

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
	print(bidders[0].getDesiredPlayers(players)[10].getPerformance())

	costHist,evalHist=gradientDescent(bidders,players,players[1])

	plt.plot(costHist)
	#plt.show()
	for row in evalHist.values():
		pass

		#plt.plot(row)
	plt.show()


if __name__ == "__main__":
    main()