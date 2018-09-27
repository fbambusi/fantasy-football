fore<-function(name)
{
  verdi=subset(all_days_with_fantasy_evaluation,Nome==name)
  
  verdi <- verdi[with(verdi,order(verdi$Year,verdi$Day)) , ]
  ts<-verdi[c("Day","FantasyEvaluation","Voto")]
  ts$z <- c(NA,diff(ts$FantasyEvaluation))
  voti<-scale(ts$FantasyEvaluation,scale=FALSE)
  mod<-auto.arima(voti)
  
  val<-forecast(mod,1)$mean[1]
  delta<-mean(ts$z[-1])+val
  fore<-tail(verdi$FantasyEvaluation, n=1)+delta
  return(fore)
}

trivial_predictor<-function(name){
  return (mean( subset(all_days_with_fantasy_evaluation,Nome==name)$FantasyEvaluation )  );
}

mine<-as.data.frame(unique(subset(players_synthesis_by_me,Owner=="ME")$Name))
res<-apply(mine,1,fore)


triv<-apply(mine,1,trivial_predictor)
  
mine$fore=as.data.frame(res)
mine$triv=as.data.frame(triv)
