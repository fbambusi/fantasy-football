quotazioni<-quotazioni[,c(3,5,6)]
tmp<-merge(quotazioni,players_synthesis_by_me,by="Name")
plot(tmp$Qt..I,tmp$WeightedFantasyEvaluation)
scatter.smooth(x=cars$speed, y=cars$dist, main="Dist ~ Speed")
tmp<-tmp[,c(3,10)]
lm(tmp)
#rsquare=0,45
transform(tmp,square=WeightedFantasyEvaluation^2)

linear2<-lm(sqr)
#rsquare 0,55

tmp<-transform(tmp,cmc=WeightedFantasyEvaluation^3)
cbc<-cbc[,c(1,4)]
summary(lm(cbc))
#rqsuare=0,61


 tmp<-transform(tmp,quotation_log=log(Qt..I))
 logar<-tmp[,c(2,4)]
 summary(lm(logar))
 #rqsuare=0,47
 
 tmp<-transform(tmp,frt=WeightedFantasyEvaluation^4)
 frt<-tmp[,c(1,5)]
 summary(lm(frt))
 #rqsuare=0,63
 
 
 scatter.smooth(x=logar$Qt..I, y=logar$quotation_log, main="Dist ~ Speed")
 