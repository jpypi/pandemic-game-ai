#!/usr/bin/env python3

import csv

from player import Player
from city import City
from cards import PlayerCard, PlayerCardDeck, ShuffleDeck
from game import Game
import helper_ai


class Graph:
    def __init__(self, nodes) :
        # Store the adjacency list as a dictionary
        # 0 : { 1, 2 }
        # 1 : { 3, 4 }
        self.adjlist = {}
        self.nodes = nodes

    # Assuming that the edge is bidirectional
    def AddEdge (self, src, dst) :

        if src not in self.adjlist :
            self.adjlist[src] = []

        if dst not in self.adjlist :
            self.adjlist[dst] = []

        self.adjlist[src].append(dst)
        #self.adjlist[dst].append(src) not needed for my case

    def GetNeighbors(self, src):
        return self.adjlist[src]

    def Display_AdjList(self) :
        for item in self.adjlist.items() :
            print (item)


if __name__ == "__main__" :
    #main area
    test_game = Game(4,'hard',None)

    test_game.print_game_state()

    print("testing probability distribution")
    print(helper_ai.calculate_drawing_infection_city_card(test_game,test_game.get_city_by_name('Atlanta')))

    print("outbreak chance is " + str(helper_ai.calculate_probability_of_outbreak(test_game)))
    """
    #Step 2: construct the graph
    map = Graph(len(city_list))
    city_id_to_name = {}
    city_name_to_id = {}
    for c in city_list:
        # create a dictionary of the city ID to name and a dictionary of name to ID
        real_id = int(c.ID)-1
        city_id_to_name[real_id] = c.name
        city_name_to_id[c.name] = real_id
        for d in c.neighbors:
            map.AddEdge(real_id,int(d)-1)

    print("adjaceny list for storing graph")
    #map.Display_AdjList()
    """


    """
    #Display which cities have infection and research stations
    print("====================")
    print("Diseased Cities List")
    for c in city_list:
        c.ShowDiseaseStatus()
    print("====================")
    print("Research Center List")
    for c in city_list:
        c.ShowResearchCenterStatus()
    print("====================")
    print("Players")
    #display player cards and roles
    for p in player_list:
        p.ShowCharacter(city_list)
        p.ShowActionOptions(city_list, player_list, None)
    print("====================")
    #--------
    #Print a demo players options
    """
