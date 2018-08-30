players_synthesis_by_me <- read.csv("C:/Users/asus/Desktop/Poli/fantasy-football/dataset/players_synthesis_by_me.csv")
attackers<-subset(players_synthesis_by_me,Role=="A")
goalkeepers<-subset(players_synthesis_by_me,Role=="P")
defenders<-subset(players_synthesis_by_me,Role=="D")
midfielders<-subset(players_synthesis_by_me,Role=="C")
coaches<-subset(players_synthesis_by_me,Role=="COACH")
write.csv(attackers,C:/Users/asus/Desktop/Poli/fantasy-football/dataset/views/attackers.csv)
write.csv(defender,"C:/Users/asus/Desktop/Poli/fantasy-football/dataset/views/defenders.csv");
write.csv(midfielders,"C:/Users/asus/Desktop/Poli/fantasy-football/dataset/views/midfielders.csv");
write.csv(goalkeepers,"C:/Users/asus/Desktop/Poli/fantasy-football/dataset/views/goalkeepers.csv");
write.csv(coaches,"C:/Users/asus/Desktop/Poli/fantasy-football/dataset/views/coaches.csv");