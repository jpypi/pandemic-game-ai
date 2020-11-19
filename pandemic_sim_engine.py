#!/usr/bin/env python3

import csv

from player import Player
from city import City
from cards import PlayerCard, PlayerCardDeck, ShuffleDeck


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


def CheckForOutbreaks(city_list):
    total = 0
    for city in city_list:
        if city.outbreaked:
            total += 1
            city.outbreaked = False


def SpawnEpidemic(infected_discard, infection_cards, epidemics_occured, city_list, players):
    epidemics_occured += 1
    infection_options = [2,2,2,3,3,4,4]
    infection_rate = infection_options[epidemics_occured]
    bottom_card = infection_cards.pop(-1)
    city_list[bottom_card.ID].AddDrawnInfection(city_list,3,players)
    infected_discard.append(bottom_card)
    #reshuffle discard
    ShuffleDeck(infected_discard)
    #stick back on top
    #need to return basically everything?
    return infected_discard.extend(infection_cards)


if __name__ == "__main__" :
    #main area
    city_list = []
    #Step 1: import all the cities from csv
    fn = 'pandemic_cities.csv'
    with open(fn) as csvfile:
        cityreader = csv.reader(csvfile)
        #todo insert try/catch
        for row in cityreader:
            neighbors = row[3:]
            ID, name, color = int(row[0]), row[1], row[2]
            city_list.append(City(ID, name, color, neighbors))
        #print(row[1])

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

    #Initialize Game
    role_deck = ['Medic',
                 'Researcher',
                 'Operations Expert',
                 'Dispatcher',
                 'Quarantine Specialist',
                 'Scientist',
                 'Contingency Planner']
    ShuffleDeck(role_deck)
    print(role_deck)
    city_cards = []
    for city in city_list:
        city_cards.append(PlayerCard('city', city.name, city.ID))


    infection_cards = city_cards
    ShuffleDeck(infection_cards)

    player_cards = PlayerCardDeck(city_cards)
    player_card_discard = []
    infection_discard = []
    player_list = []

    #Set initial infections -> clean this section up and make it its own function to initialize
    for k in range(9):
        print(city_list[infection_cards[k].ID].name)
    #set of 3s
    city_list[infection_cards[0].ID].AddDrawnInfection(city_list, 3, player_list)
    city_list[infection_cards[1].ID].AddDrawnInfection(city_list, 3, player_list)
    city_list[infection_cards[2].ID].AddDrawnInfection(city_list, 3, player_list)
    #set of 2s
    city_list[infection_cards[3].ID].AddDrawnInfection(city_list, 2, player_list)
    city_list[infection_cards[4].ID].AddDrawnInfection(city_list, 2, player_list)
    city_list[infection_cards[5].ID].AddDrawnInfection(city_list, 2, player_list)
    #set of 1s
    city_list[infection_cards[6].ID].AddDrawnInfection(city_list, 1, player_list)
    city_list[infection_cards[7].ID].AddDrawnInfection(city_list, 1, player_list)
    city_list[infection_cards[8].ID].AddDrawnInfection(city_list, 1, player_list)
    #discard these to discard pile
    infection_discard.append(infection_cards.pop(0))
    infection_discard.append(infection_cards.pop(1))
    infection_discard.append(infection_cards.pop(2))
    infection_discard.append(infection_cards.pop(3))
    infection_discard.append(infection_cards.pop(4))
    infection_discard.append(infection_cards.pop(5))
    infection_discard.append(infection_cards.pop(6))
    infection_discard.append(infection_cards.pop(7))
    infection_discard.append(infection_cards.pop(8))

    #Set number of players
    num_of_players = 4
    player_list.append(Player(role_deck[0], "Kevin", 0))
    player_list.append(Player(role_deck[2], "Megan", 1))
    player_list.append(Player(role_deck[1], "Phil", 2))
    player_list.append(Player(role_deck[3], "Jesse", 3))

    #Draw Player Cards
    start_cards = player_cards.DrawPlayerStartingCards(num_of_players)
    c = 0
    for p in player_list:
        for k in range(len(start_cards[c])):
            p.AddCard(start_cards[c][k])
        c += 1

    #Add in epidemic Cards
    num_of_epidemics = 6 #between 4 and 6
    epidemics_occured = 0

    player_cards.AddEpidemicCards(num_of_epidemics)

    #Add research station to atlanta
    city_list[0].research_center = True

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
        p.ShowActionOptions(city_list, map, player_list, None)
    print("====================")
    #--------
    #Print a demo players options

    #Example Round
    #Player does action
    #player draws 2 cards
    #player draws 2 infections
    #player increments outbreak counter
