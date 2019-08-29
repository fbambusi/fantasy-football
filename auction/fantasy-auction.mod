set Bidders= 1..8 by 1;
set Players;
set Roles;
set CompatibilityPlayerRole within {Players,Roles};
set Slots=1..25 by 1;
set CompatibilitySlotRole within {Slots,Roles};

param multiplier{Slots} default 1;
param performance{Players};
param cost{Players};
param alreadyBought{Players} binary;

param maxPlayers{Roles};

var buy{Bidders,Players} binary;
var putPlayerInSlot{Bidders,Players,Slots} binary;

var perf{Bidders};
var minPerf;


maximize mp:minPerf;



s.t. slotCanBeOccupiedByCompatiblePlayersOnly {bidder in Bidders,player in Players,slot in Slots}:
	putPlayerInSlot[bidder,player,slot]<=sum{(player,role) in CompatibilityPlayerRole}sum{(slot,role) in CompatibilitySlotRole}1;

s.t. slotCanBeOccupiedByBoughtPlayersOnly{bidder in Bidders,player in Players,slot in Slots}:
	putPlayerInSlot[bidder,player,slot]<=buy[bidder,player];

s.t. playersCanHaveAtMostOneOwner{player in Players}:
	sum{bidder in Bidders} buy[bidder,player]<=1;

s.t. playersCanBePutInAtMostOneSlot{player in Players}:
	sum{bidder in Bidders,slot in Slots} putPlayerInSlot[bidder,player,slot] <=1;

s.t. definitionOfPerformance{bidder in Bidders}:
	perf[bidder]= sum{player in Players,slot in Slots}performance[player]*putPlayerInSlot[bidder,player,slot]*multiplier[slot];

s.t. definitionOfMinPerf{bidder in Bidders}:
	minPerf<=perf[bidder];