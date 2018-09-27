tot=merge(all_days_tmp_with_fantasy_evaluation,Statistiche_Fantacalcio_2017.18_Fantagazzetta,by="Nome")
tot2<-merge(tot,calendar2017.2018,by=c("Squadra","Day"))
in_casa<-subset(tot2,SquadraCasa==1)
fuori_casa<-subset(tot2,SquadraCasa==0)
s_in<-in_casa[,c(3,6,20,38)]
s_out<-fuori_casa[,c(3,6,20,38)]
comparison<-merge(s_in,s_out,by=c("Nome","Avversario"))
t.test(comparison$Voto.x,comparison$Voto.y,paired=TRUE,alternative = "greater")