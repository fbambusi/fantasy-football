set Players;
set Roles;
set Modules;

set CompatibilityPlayerRole within {Players,Roles};
set Slots=1..32 by 1;
set CompatibilitySlotRole within {Modules,Slots,Roles};

param multiplier{Modules,Slots} default 1;
param performance{Players};
param cost{Players};

param alreadyBoughtByOther{Players} binary default 0;
param alreadyBoughtByMe{Players} binary default 0;

var buy{Players} binary;
var putPlayerInSlot{Modules,Players,Slots} binary;
var bidderChoosesModule{Modules} binary;

var performanceofModule{Modules};
var minPerf;

param perfBigM=10000;

param budget default 500;

param minPlayersInRole{Roles} default 2;

maximize mp:minPerf;


s.t. biddersMustChooseOneModule:
	sum{module in Modules}bidderChoosesModule[module]=1;

s.t. definitionOfPerformanceOfModule{module in Modules}:
	performanceofModule[module]<=sum{slot in Slots,player in Players}performance[player]*putPlayerInSlot[module,player,slot]*multiplier[module,slot];

s.t. slotCanBeOccupiedByCompatiblePlayersOnly {player in Players,slot in Slots,module in Modules}:
	putPlayerInSlot[module,player,slot]<=sum{(player,role) in CompatibilityPlayerRole}sum{(module,slot,role) in CompatibilitySlotRole}1;

s.t. slotCanBeOccupiedByBoughtPlayersOnly{player in Players,slot in Slots,module in Modules}:
	putPlayerInSlot[module,player,slot]<=buy[player]+alreadyBoughtByMe[player];

s.t. playersCanHaveAtMostOneOwner{player in Players}:
	buy[player]<=1-alreadyBoughtByOther[player];

s.t. defintionOfPerformanceOfBidder{module in Modules}:
	minPerf<=performanceofModule[module]+(1-bidderChoosesModule[module])*perfBigM;

s.t. playersCanBePutInAtMostOneSlot{player in Players}:
	sum{slot in Slots,module in Modules} putPlayerInSlot[module,player,slot] <=1;

s.t. biddersCanFillEachSlotAtMostOnce{slot in Slots,module in Modules}:
	sum{player in Players}putPlayerInSlot[module,player,slot]<=1;

s.t. modulesNotChosenAreEmpty{module in Modules,player in Players, slot in Slots}:
	putPlayerInSlot[module,player,slot]<=bidderChoosesModule[module];

s.t. boughtPlayersMustBeUsed{player in Players}:
	buy[player]<=sum{module in Modules,slot in Slots} putPlayerInSlot[module,player,slot];

s.t. budgetConstraint:
	sum{player in Players}buy[player]*cost[player]<=budget;

s.t. minNumberOfPlayersInRole{role in Roles}:
	sum{(player,role) in CompatibilityPlayerRole}buy[player]>=minPlayersInRole[role];