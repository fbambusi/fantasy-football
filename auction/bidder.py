import random

class bidder:
	def __init__(self,budget):
		self.ownedPlayers=[]
		self.budget=budget
		self.adaptivity=random.random()+1
	def getBoughtPlayers(self):
		return []
	def buyPlayer(self,player,price):
		self.ownedPlayers.append(player)
		self.budget-=price
		return

	def getOwnedPlayers(self):
		return self.ownedPlayers

	def getNumberOfOwnedPlayers(self):
		return len(self.ownedPlayers)

	def getBudget(self):
		return self.budget

	def setBudget(self,budget):
		self.budget=budget

	def canPay(self,price):
		return self.budget>=price
	def getDesiredPlayers(self,playersList):
		self.availablePlayers=playersList
		self.desiredPlayers=playersList[:30]
		return playersList[:30]

	def getValueOfPlayers(self):
		return self.values

	def correctValueOfPlayer(self,playerName,correction):
		self.values[playerName]+=correction
		if self.values[playerName]<1:
			self.values[playerName]=1

	def correctValueOfPlayers(self,winner,learning_rate):
		for playerName in self.values.keys():
			self.values[playerName]+=(winner.getValueOfPlayers()[playerName]-self.values[playerName])*(self.adaptivity)
			if self.values[playerName]<1:
				self.values[playerName]=1
			if self.values[playerName]>self.budget:
				self.values[playerName]=self.adaptivity*self.budget
				
	def randomlyCorrectValueOfPlayers(self,learning_rate,budget):
		oldPrice=0
		for playerName in self.values.keys():
			self.values[playerName]+=(random.random()-0.5)*learning_rate*8+(oldPrice-self.values[playerName])*learning_rate/8

			if self.values[playerName]>budget:
				self.values[playerName]=budget
			if self.values[playerName]<=0:
				self.values[playerName]=0
			oldPrice=self.values[playerName]

	def resetOwnedPlayers(self):
		self.ownedPlayers=[]

	def randomizeEvaluation(self,playersList):
		evals={}
		currEval=(random.random()+1)*100
		for player in playersList:
			currEval+=random.random()+1
			evals[player.getName()]=currEval
		self.values=evals

	def getPerformanceOfTeam(self):
		return sum(map(lambda p:p.getPerformance(),self.ownedPlayers))