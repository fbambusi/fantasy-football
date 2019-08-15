import random

class bidder:
	def __init__(self):
		self.ownedPlayers=[]
	def getBoughtPlayers(self):
		return []
	def buyPlayer(self,player,price):
		self.ownedPlayers.append(player)
		self.budget-=price
		return
	def getOwnedPlayers(self):
		return self.ownedPlayers
	def getBudget(self):
		return 1
	def setBudget(self,budget):
		self.budget=budget
	def getDesiredPlayers(self,playersList):
		self.availablePlayers=playersList
		self.desiredPlayers=playersList[:30]
		return playersList[:30]

	def getValueOfPlayers(self):
		return self.values

	def correctValueOfPlayer(self,playerName,correction):
		self.values[playerName]+=correction

	def correctValueOfPlayers(self,winner,learning_rate):
		for playerName in self.values.keys():
			self.values[playerName]+=(winner.getValueOfPlayers()[playerName]-self.values[playerName])*learning_rate
		
	def randomlyCorrectValueOfPlayers(self,learning_rate):
		for playerName in self.values.keys():
			self.values[playerName]+=random.random()*learning_rate/10

	def resetOwnedPlayers(self):
		self.ownedPlayers=[]
	def randomizeEvaluation(self,playersList):
		evals={}
		for player in playersList:
			evals[player.getName()]=random.random()
		self.values=evals

	def getPerformanceOfTeam(self):
		return sum(map(lambda p:p.getPerformance(),self.ownedPlayers))