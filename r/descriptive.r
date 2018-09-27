pippo<-aggregate(as.numeric(as.character(all_days$Voto)), by=list(all_days$Nome),FUN=mean)
#This index is probably less interesting than a one taking into account the number of
#matches played, since it's pointless buying smn with a unique, great performance
pippo<-aggregate(as.numeric(as.character(all_days$FantasyEvaluation)), by=list(all_days$Nome),FUN=mean)
colnames(pippo)[colnames(pippo) == 'Group.1'] <- 'Name'
colnames(pippo)[colnames(pippo) == 'x'] <- 'MeanFantasyEvaluation'

players_synthesis_by_me$MeanFantasyEvaluation<-NULL
players_synthesis_by_me<-merge(players_synthesis_by_me,pippo,by="Name")
write.csv(players_synthesis_by_me,"C:/Users/asus/Desktop/Poli/fantasy-football/dataset/players_synthesis_by_me.csv")

#Not totally useless, however, since it could represent the mark taken by player 
#when he plays
presenze<-table(all_days$Nome)
#Necessary to edit
as.data.frame(presenze)

#Append to variance (table) the second row of variable "presenze"
variance<-cbind(variance,presenze[,2])

#select by role