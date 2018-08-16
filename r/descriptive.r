aggregate(as.numeric(as.character(all_days$Voto)), by=list(all_days$Nome),FUN=mean)
#This index is probably less interesting than a one taking into account the number of
#matches played, since it's pointless buying smn with a unique, great performance

#Not totally useless, however, since it could represent the mark taken by player 
#when he plays