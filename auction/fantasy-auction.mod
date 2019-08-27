set Bidders= 1..8 by 1;
set Players;
set Roles;
set CompatibilityPlayerRole within {Players,Roles};

param performance{Players};
param cost{Players};
param budget;
param alreadyBought{Players} binary;

param maxPlayers{Roles};
var buy{Bidders,Players} binary;
var perf{Bidders};
var minPerf;

maximize mp:minPerf;


s.t. budgetConstraint{bidder in Bidders}:
	sum{player in Players} buy[bidder,player]*cost[player]<=budget;

s.t. maxPlayersConstraint {role in Roles,bidder in Bidders}:
	sum{(player,role) in CompatibilityPlayerRole} buy[bidder,player] <=maxPlayers[role];

s.t. playersCanHaveAtMostOneOwner{player in Players}:
	sum{bidder in Bidders} buy[bidder,player]<=1;

s.t. definitionOfPerformance{bidder in Bidders}:
	perf[bidder]= sum{player in Players}performance[player]*buy[bidder,player];

s.t. definitionOfMinPerf{bidder in Bidders}:
	minPerf<=perf[bidder];