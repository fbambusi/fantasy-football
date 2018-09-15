from scipy.stats import norm
from show_precise_roles import *

def probability_team_1_loss(team1_components,team2_components):
	avg=0
	variance=0
	for player in team1_components:
		avg=avg+float(player["MeanFantasyEvaluation"])
		try:
			variance_tmp=float(player["VarianceFantasyEvaluation"])
		except ValueError:
			variance_tmp=0
		variance=variance+variance_tmp
	for player in team2_components:
		avg=avg-float(player["MeanFantasyEvaluation"])
		try:
			variance_tmp=float(player["VarianceFantasyEvaluation"])
		except ValueError:
			variance_tmp=0
		variance=variance+variance_tmp

	distro=norm(avg, variance**0.5)
	mean=distro.stats(moments="m")
	loss=distro.cdf(-6)
	draw=distro.cdf(6)-loss
	win=1-distro.cdf(6)
	return loss,draw,win

def players_from_file(filename,players_dict):
	file_=open("opponents/"+filename,"r")
	data=file_.readlines()
	all=[]
	for player_name in data:
		all.append(players_dict[player_name.strip()])
	return all

def compare(t1,t2,players_dict):
	
	team_me=players_from_file(t1,players_dict)
	team_gatti=players_from_file(t2,players_dict)
	loss,draw,win=probability_team_1_loss(team_me,team_gatti)	
	print("Match:" +t1+" vs "+ t2)
	print("    1:"+str(1/win)+"    x:"+str(1/draw)+"     2:"+str(1/loss))

def main():
	players_dict=get_players_dict()
	compare("me1.txt","gatti1.txt",players_dict)
	compare("ve1.txt","bryan1.txt",players_dict)
main()