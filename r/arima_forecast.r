#http://ucanalytics.com/blogs/step-by-step-graphic-guide-to-forecasting-through-arima-modeling-in-r-manufacturing-case-study-example/
verdi=subset(all_days_with_fantasy_evaluation,Nome=="ICARDI")

verdi <- verdi[with(verdi,order(verdi$Year,verdi$Day)) , ]

plot(verdi$Day,verdi$FantasyEvaluation)
ts<-verdi[c("Day","FantasyEvaluation","Voto")]
ts$z <- c(NA,diff(ts$FantasyEvaluation))
voti<-scale(ts$FantasyEvaluation,scale=FALSE)
acf(ts(ts$z),na.action = na.pass)
mod<-auto.arima(voti)
summary(mod)
var(ts$z)

acf(ts(residuals(mod)),na.action=na.pass)
val<-forecast(mod,1)$mean[1]
delta<-mean(ts$z[-1])+val
fore<-tail(verdi$FantasyEvaluation, n=1)+delta

