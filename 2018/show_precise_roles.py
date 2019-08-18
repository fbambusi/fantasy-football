from download_dataset import *
import csv
import copy
import networkx as nx

class Slot:
    def __init__(self,allowed_roles,required_players):
        self.allowed_roles=allowed_roles
        self.occupiers=[]
        self.required_players=required_players

    def occupy(self,player):
        if player["MantraRole"] in self.allowed_roles:
            self.occupiers.append(player)
    def show(self):
        print(self.allowed_roles)
        for player in self.occupiers:
            print(player["Name"]+"   "+player["MeanFantasyEvaluation"]) 
    def compatible(self,player):
        for role in player["MantraRole"]:
            if role in self.allowed_roles:
                return True
        return False
    def name(self):
        return "/".join(self.allowed_roles)

"""This class represents the disposition a team can have during a match"""
class MantraSelection:
    def __init__(self,slots):
        self.slots=slots

    def insert(self,player):
        for slot in self.slots:
            slot.occupy(player)
    def fill(self,players):
        for player in players:
            self.insert(player)
    def show(self):
        for slot in self.slots:
           slot.show()


"""Version for ortools-64b machines only :("""
class GoogleGraphBluePrint:
    def __init__(self,selection,players):
        start_nodes=[]
        end_nodes=[]
        capacities=[]
        unit_costs=[]
        
        num_players=len(players)
        num_roles=len(selection.slots)
        """Draw a line from source to each player"""
        for i in range(1,num_players+1):
            start_nodes.append(0)
            end_nodes.append(i)
            capacities.append(1)
            unit_costs.append(-players[i]["MeanFantasyEvaluation"])

        """Draw a line from each player to every role he's compatible with"""
        for i in range(1,num_players+1):
            for j in range(num_players+1,num_players+1+num_roles):
                if selection.slots[j].compatible(players[i]):
                    start_nodes.append(i)
                    end_nodes.append(j)
                    capacities.append(1)
                    unit_costs.append(0)

        """Draw a line from each role to the sink. Capacity is the number of required players"""
        for j in range(num_players+1,num_players+1+num_roles):
            start_nodes.append(j)
            end_nodes.append(num_players+1+num_roles)
            capacities.append(slots[j-num_players-1].required_players)
            unit_costs.append(0)

        """Connect sink to source so as to create a pump"""
        start_nodes.append(num_players+1+num_roles)
        end_nodes.append(0)
        capacities.append(num_players+100)
        unit_costs.append(0)

class GraphBlueprint:
    def __init__(self,selection,players):
        graph = nx.DiGraph()
        graph.add_node("source",demand=0)
        for player in players:
            graph.add_node(player["Name"],demand=0)
        for slot in selection.slots:
            graph.add_node(slot.name(),demand=0)
        graph.add_node("sink",demand=0)

        for player in players:
            graph.add_edge("source",player["Name"],weight=0,capacity=1)
        for player in players:
            for slot in selection.slots:
                if slot.compatible(player):
                    graph.add_edge(player["Name"],slot.name(),weight=-1*float(player["Value"]),capacity=1)

        for slot in selection.slots:
            graph.add_edge(slot.name(),"sink",weight=0,capacity=slot.required_players)

        graph.add_edge("sink","source",weight=0,capacity=len(players)+100)
        flowCost, flowDict = nx.network_simplex(graph)
        self.roles=flowDict

#this method returns mean and variance of a list of players
def  distribution(player_list,attribute="MeanFantasyEvaluation"):
    value=0
    variance=0
    for player in player_list:
        value=value+float(player[attribute])
        try:
            variance_tmp=float(player["VarianceFantasyEvaluation"])
        except ValueError:
            variance_tmp=0
        variance=variance+variance_tmp
    return value,variance

def  get_players():
    attackers_file=open(PLAYER_SYNTHESIS)
    player_dict={}
    player_list=csv.DictReader(attackers_file)
    all=[]
    for player in player_list:
        if player["Name"] not in player_dict:
            player["MantraRole"]=[player["MantraRole"]]
            player_dict[player["Name"]]=player
            all.append(player)
        else:
            player_dict[player["Name"]]["MantraRole"].append(player["MantraRole"])

    return all

def get_players_dict():
    attackers_file=open(PLAYER_SYNTHESIS)
    player_dict={}
    player_list=csv.DictReader(attackers_file)
    all=[]
    for player in player_list:
        if player["Name"] not in player_dict:
            player["MantraRole"]=[player["MantraRole"]]
            player_dict[player["Name"]]=player
            all.append(player)
        else:
            player_dict[player["Name"]]["MantraRole"].append(player["MantraRole"])

    return player_dict

def my_players():
    players=get_players()
    my_players=filter(lambda p:p["Owner"]=="ME",players)
    return sorted(my_players,key=lambda p:p["MeanFantasyEvaluation"],reverse=True)

def main():
    my_p=my_players()

    slots=[]
    slots.append(Slot(["A","W"],2))
    slots.append(Slot(["A","Pc"],1))
    slots.append(Slot(["E"],2))
    slots.append(Slot(["M","C"],2))
    slots.append(Slot(["Dc"],3))
    slots.append(Slot(["Por"],1))

    for player in my_p:
        player["Value"]=player["WeightedFantasyEvaluation"]
    my343=MantraSelection(slots)
    my343.fill(my_p)

    flow=GraphBlueprint(my343,my_p)
    holders=[]
    for player in flow.roles:
        for role in flow.roles[player]:
            if flow.roles[player][role]>0 and role!="sink" and role!="source" and player!="source" and player!="sink":
                print(player+"   gioca come    "+role)
                holders.append(player)
    
    print("=======================================================================")

    next=[]
    for player in my_p:
        if player["Name"] not in holders:
            next.append(player)
    flow=GraphBlueprint(my343,next)
    for player in flow.roles:
        for role in flow.roles[player]:
            if flow.roles[player][role]>0 and role!="sink" and role!="source" and player!="source" and player!="sink":
                print(player+"   gioca come    "+role)
                holders.append(player)
    next=[]
    for player in my_p:
        if player["Name"] not in holders:
            next.append(player)
    next=sorted(next,key=lambda p:p["WeightedFantasyEvaluation"],reverse=True)
    for p in next:
        print(p["Name"]+"     :")
        for r in p["MantraRole"]:
            print("            "+r)
if __name__ == "__main__":
    main()


#https://www.fantagazzetta.com/Servizi/Ultimi11.ashx?id=3015&tv=273627688600&ts=273844040992&g=3&ids=13