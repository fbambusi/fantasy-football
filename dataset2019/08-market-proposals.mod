set Players;
set Roles;
set Modules;

set CompatibilityPlayerRole within {Players,Roles};
set Slots=1..28 by 1;
set CompatibilitySlotRole within {Modules,Slots,Roles};

param multiplier{Modules,Slots} default 1;
param performance{Players};
param ownedByMe{Players} binary default 0;
param cost{Players};
param broken{Players} binary default 0;


var iPutPlayerInSlot{Modules,Players,Slots} binary;
var iChoosesModule{Modules} binary;

var adversaryPutPlayerInSlot{Modules,Players,Slots} binary;
var adversaryChoosesModule{Modules} binary;

var iPerformanceofModule{Modules};
var advPerformanceOfModule{Modules};
var minPerf;
var switched{Players} binary;

var minPerfOfMine;
var minePrfOfAdv;

param perfBigM=10000;

param initialPerformanceOfMe default 84.32151607;
param initialPerformanceOfAdversary default 75.28095488;
param maxPlayersToSwitch default 8;



maximize mp:minPerf;


s.t. biddersMustChooseOneModule:
	sum{module in Modules}iChoosesModule[module]=1;


s.t. adversaryMustChooseOneModule:
	sum{module in Modules}adversaryChoosesModule[module]=1;

s.t. iDefinitionOfPerformanceOfModule{module in Modules}:
	iPerformanceofModule[module]<=sum{slot in Slots,player in Players}performance[player]*iPutPlayerInSlot[module,player,slot]*multiplier[module,slot];


s.t. adversaryDefinitionOfPerformanceOfModule{module in Modules}:
	advPerformanceOfModule[module]<=sum{slot in Slots,player in Players}performance[player]*adversaryPutPlayerInSlot[module,player,slot]*multiplier[module,slot];


s.t. iSlotCanBeOccupiedByCompatiblePlayersOnly {player in Players,slot in Slots,module in Modules}:
	iPutPlayerInSlot[module,player,slot]<=sum{(player,role) in CompatibilityPlayerRole}sum{(module,slot,role) in CompatibilitySlotRole}1;


s.t. advSlotCanBeOccupiedByCompatiblePlayersOnly {player in Players,slot in Slots,module in Modules}:
	adversaryPutPlayerInSlot[module,player,slot]<=sum{(player,role) in CompatibilityPlayerRole}sum{(module,slot,role) in CompatibilitySlotRole}1;


s.t. advBrokenPlayersCannotPlay{player in Players,slot in Slots,module in Modules}:
	adversaryPutPlayerInSlot[module,player,slot]<=1-broken[player];


s.t. iBrokenPlayersCannotPlay{player in Players,slot in Slots,module in Modules}:
	iPutPlayerInSlot[module,player,slot]<=1-broken[player];



s.t. iDefintionOfPerformanceOfBidder{module in Modules}:
	minPerfOfMine<=iPerformanceofModule[module]+(1-iChoosesModule[module])*perfBigM;

s.t. advDefintionOfPerformanceOfBidder{module in Modules}:
	minePrfOfAdv<=advPerformanceOfModule[module]+(1-adversaryChoosesModule[module])*perfBigM;


s.t. iPlayersCanBePutInAtMostOneSlot{player in Players}:
	sum{slot in Slots,module in Modules} iPutPlayerInSlot[module,player,slot] <=1;

s.t. adversaryPlayersCanBePutInAtMostOneSlot{player in Players}:
	sum{slot in Slots,module in Modules} adversaryPutPlayerInSlot[module,player,slot] <=1;



s.t. iBiddersCanFillEachSlotAtMostOnce{slot in Slots,module in Modules}:
	sum{player in Players}iPutPlayerInSlot[module,player,slot]<=1;

s.t. advBiddersCanFillEachSlotAtMostOnce{slot in Slots,module in Modules}:
	sum{player in Players}adversaryPutPlayerInSlot[module,player,slot]<=1;

s.t. conven:
	minPerfOfMine>=initialPerformanceOfMe;

s.t. c2:
	minePrfOfAdv>=initialPerformanceOfAdversary;

s.t. maxNumberOfSwitches:
	sum{player in Players}switched[player]<=maxPlayersToSwitch;

s.t. iUsabilityOfPlayers{player in Players,slot in Slots,module in Modules}:
	iPutPlayerInSlot[module,player,slot]<=ownedByMe[player]*(1-switched[player])+switched[player]*(1-ownedByMe[player]);


s.t. advUsabilityOfPlayers{player in Players,slot in Slots,module in Modules}:
	adversaryPutPlayerInSlot[module,player,slot]<=(1-ownedByMe[player])*(1-switched[player])+switched[player]*(ownedByMe[player]);

s.t. minPerfDef:
	minPerf<=minPerfOfMine;

s.t. minPerfOfMined:
	minPerf<=minePrfOfAdv;

s.t. fairTrade:
	sum{player in Players}switched[player]*ownedByMe[player]=sum{p2 in Players}switched[p2]*(1-ownedByMe[p2]);