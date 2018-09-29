player_model<-function(name)
{
  verdi=subset(all_days_with_fantasy_evaluation,Nome==name)
  
  verdi <- verdi[with(verdi,order(verdi$Year,verdi$Day)) , ]
  ts<-verdi[c("Day","FantasyEvaluation","Voto")]
  ts$z <- c(NA,diff(ts$FantasyEvaluation))
  mod<-auto.arima(scale(ts$z,scale=FALSE))
  return(mod);
  
}

err<-function(mod)
{
  return (var(mod$residuals,na.rm=TRUE));
}

fore<-function(mod)
{
  val<-forecast(mod,1)$mean[1]
  delta<-mean(ts$z[-1])+val
  fore<-tail(verdi$FantasyEvaluation, n=1)+delta
  return(fore)
}


trivial_predictor<-function(name){
  return (mean( subset(all_days_with_fantasy_evaluation,Nome==name)$FantasyEvaluation )  );
}

trivial_error<-function(name){
  return (var( subset(all_days_with_fantasy_evaluation,Nome==name)$FantasyEvaluation )  );
}
mine<-as.data.frame(unique(subset(players_synthesis_by_me,Owner=="ME")$Name))

mods<-apply(mine,1,player_model)

res<-lapply(mods,fore)

triv<-apply(mine,1,trivial_predictor)
arima_err<-lapply(mods,err)
triv_err<-apply(mine,1,trivial_error)

mine$fore=t(as.data.frame(res))
mine$triv=as.data.frame(triv)
mine$err_arima=t(as.data.frame(arima_err))
mine$triv_err=as.data.frame(triv_err)

