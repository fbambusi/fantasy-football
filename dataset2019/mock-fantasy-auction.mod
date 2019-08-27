reset;
model fantasy-auction.mod;
data fantasy-auction-mock.dat;
option solver "/home/asino/Downloads/ampl_linux-intel64/cplex";
solve;
display buy;