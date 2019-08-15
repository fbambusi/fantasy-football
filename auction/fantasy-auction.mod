set Players;
set Roles;
set CompatibilityPlayerRole within {Players,Roles};

param performance{Players};
param cost{Players};
param budget;
param alreadyBought{Players};

param maxPlayers{Roles};
var buy{Players} binary;


maximize perf: sum{player in Players}performance[player]*buy[player];


s.t. budgetConstraint:
	sum{player in Players} buy[player]*cost[player]<=budget;

s.t. maxPlayersConstraint {role in Roles}:
	sum{(player,role) in CompatibilityPlayerRole} buy[player] <=maxPlayers[role];


s.t. playersCannobBeBoughtTwice{player in Players}:
	buy[player]<=1-alreadyBought[player];

