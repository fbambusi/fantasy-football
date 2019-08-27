set Bidders= 1..6 by 1;
set Players;
set Roles;
set Modules;

set CompatibilityPlayerRole within {Players,Roles};
set Slots=1..25 by 1;
set CompatibilitySlotRole within {Modules,Slots,Roles};

param multiplier{Modules,Slots} default 1;
param performance{Players};
param cost{Players};
param alreadyBought{Players} binary default 0;


var buy{Bidders,Players} binary;
var putPlayerInSlot{Modules,Bidders,Players,Slots} binary;
var bidderChoosesModule{Bidders,Modules} binary;

var performanceofModule{Bidders,Modules};
var performanceOfBidder{Bidders};
var minPerf;

param perfBigM=10000;

maximize mp:minPerf;


s.t. biddersMustChooseOneModule{bidder in Bidders}:
	sum{module in Modules}bidderChoosesModule[bidder,module]=1;

s.t. definitionOfPerformanceOfModule{bidder in Bidders,module in Modules}:
	performanceofModule[bidder,module]<=sum{slot in Slots,player in Players}performance[player]*putPlayerInSlot[module,bidder,player,slot]*multiplier[module,slot];

s.t. slotCanBeOccupiedByCompatiblePlayersOnly {bidder in Bidders,player in Players,slot in Slots,module in Modules}:
	putPlayerInSlot[module,bidder,player,slot]<=sum{(player,role) in CompatibilityPlayerRole}sum{(module,slot,role) in CompatibilitySlotRole}1;

s.t. slotCanBeOccupiedByBoughtPlayersOnly{bidder in Bidders,player in Players,slot in Slots,module in Modules}:
	putPlayerInSlot[module,bidder,player,slot]<=buy[bidder,player];

s.t. playersCanHaveAtMostOneOwner{player in Players}:
	sum{bidder in Bidders} buy[bidder,player]<=1;

s.t. defintionOfPerformanceOfBidder{bidder in Bidders,module in Modules}:
	performanceOfBidder[bidder]<=performanceofModule[bidder,module]+(1-bidderChoosesModule[bidder,module])*perfBigM;

s.t. playersCanBePutInAtMostOneSlot{player in Players}:
	sum{bidder in Bidders,slot in Slots,module in Modules} putPlayerInSlot[module,bidder,player,slot] <=1;

s.t. definitionOfMinPerf{bidder in Bidders}:
	minPerf<=performanceOfBidder[bidder];

s.t. biddersCanFillEachSlotAtMostOnce{bidder in Bidders,slot in Slots,module in Modules}:
	sum{player in Players}putPlayerInSlot[module,bidder,player,slot]<=1;

s.t. modulesNotChosenAreEmpty{bidder in Bidders,module in Modules,player in Players, slot in Slots}:
	putPlayerInSlot[module,bidder,player,slot]<=bidderChoosesModule[bidder,module];

s.t. boughtPlayersMustBeUsed{bidder in Bidders,player in Players}:
	buy[bidder,player]<=sum{module in Modules,slot in Slots} putPlayerInSlot[module,bidder,player,slot];