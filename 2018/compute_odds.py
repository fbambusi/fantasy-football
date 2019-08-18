from scipy.stats import norm
from scrape_players import *

FIRST_GOAL_SCORE=66
NEXT_GOAL=6
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
def goals(player_list):
	avg,variance=distribution(player_list)
	distro=norm(avg, variance**0.5)
	goals=[]
	prev=0
	for i in range(0,10):
		prob=distro.cdf(FIRST_GOAL_SCORE+i*NEXT_GOAL)
		goals.append(prob)
	return goals

#this method computes the probability that the team with the first goal distribution wins
#param players_list1: cdf of goals of first team
#param players_list2: cdf of goals of second team
def compare_goals(players_list1,players_list2):
	goals1=goals(players_list1)
	goals2=goals(players_list2)
	probability_first_win=0
	probability_draw=0
	for i in range(1,len(goals1)):
		probability_exact=goals1[i]-goals1[i-1]
		probability_opponent_lower=goals2[i-1]
		probability_opponent_equal=goals2[i]-goals2[i-1]

		probability_first_win=probability_first_win+probability_exact*probability_opponent_lower
		probability_draw=probability_draw+probability_exact*probability_opponent_equal
		print("If i do at least "+str(i)+"  goals i will win at "+str(probability_opponent_lower) )
	return probability_first_win,probability_draw,1- probability_draw- probability_first_win

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
	print("win:"+str(win)+"    draw:"+str(draw)+"     loss:"+str(loss))
def main():
	players_dict=get_players_dict()
	compare("me1.txt","gatti1.txt",players_dict)
	compare("ve1.txt","bryan1.txt",players_dict)
	print("=========================")
	my_p=my_formation_obj(my_players(),get_players_dict())
	goalz=goals(my_p)
	for i in range(0,len(goalz)):
		print("At least goals "+str(i+1)+"   "+str(1-goalz[i]))

	my_playerz=players_from_file("me1.txt",players_dict)
	gattis=players_from_file("gatti1.txt",players_dict)
	win,draw,lose=compare_goals(my_playerz,gattis)
	print(str(win)+"   "+str(draw)+"   "+str(lose))

main()