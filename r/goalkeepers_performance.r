gol_fatti<-aggregate(as.numeric(as.character(Statistiche_Fantacalcio_2016.17_Fantagazzetta$Gf)), by=list(Statistiche_Fantacalcio_2016.17_Fantagazzetta$Squadra),FUN=sum)
colnames(gol_fatti)[colnames(gol_fatti) == 'x'] <- 'Gf'

subiti<-aggregate(as.numeric(as.character(Statistiche_Fantacalcio_2016.17_Fantagazzetta$Gs)), by=list(Statistiche_Fantacalcio_2016.17_Fantagazzetta$Squadra),FUN=sum)
colnames(subiti)[colnames(subiti) == 'x'] <- 'Gs'

gol_fatti<-merge(gol_fatti,subiti,by="Group.1")
colnames(gol_fatti)[colnames(gol_fatti) == 'Group.1'] <- 'Squadra'
rm(subiti)

d2017<-subset(all_days_with_fantasy_evaluation,Year=="2017-18")
d2017<-merge(d2017,Statistiche_Fantacalcio_2017.18_Fantagazzetta,by="Nome")
d2017_bis<-merge(d2017,calendar2017.2018,by.x=c("Squadra.x","Day"),by.y=c("Squadra","Day"))
d2017<-d2017_bis
rm(d2017_bis)
d2017<-merge(d2017,gol_fatti,by.x=c("Avversario"),by.y=c("Squadra"))


portieri<-subset(d2017,Ruolo=="P")
cor(portieri$FantasyEvaluation,portieri$Gf.y.1) #-0.13

attacanti<-subset(d2017,Ruolo=="A")
cor(attacanti$FantasyEvaluation,attacanti$Gs.y.1) # +0.06

goalkeeper_performance<-function(name){
  curr<-subset(portieri,Nome==name)
  mod<-line(curr$Gf.y.1,curr$FantasyEvaluation)
  return (mod)
}

forecast_goalkeeper_performance<-function(mod,gf_opponent)
{
  return (mod$coefficients[1]+mod$coefficients[2]*gf_opponent)
}

forecast_error<-function(mod){
  return(var(mod$residuals))
}