import csv
import Players
import random

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

class PlayerCardDeck:
    def __init__(self, city_cards):
        self.cards = []
        self.CreatePlayerDeck(city_cards)

    def CreatePlayerDeck(self, cities):
        self.cards.append(PlayerCard('event', 'Airlift', 9999))
        self.cards.append(PlayerCard('event', 'Forecast', 9999))
        self.cards.append(PlayerCard('event', 'Resilient Population', 9999))
        self.cards.append(PlayerCard('event', 'Government Grant', 9999))
        self.cards.append(PlayerCard('event', 'Quiet Night', 9999))
        self.cards.extend(cities)
        self.cards = ShuffleDeck(self.cards)

    def AddEpidemicCards(self, number_of_epidemics):
        sliced_decks = SliceDeck(self.cards, number_of_epidemics)
        player_cards = []  # reset the player deck now
        for k in sliced_decks:
            k.append(PlayerCard('Epidemic', 'Oh Shit', 1000))
            k = ShuffleDeck(k)
            # stack back together
            player_cards.append(k)
        self.cards = player_cards

    def DrawPlayerStartingCards(self, n_players):
        if n_players == 3:
            sum = 9
        else:
            sum = 8

        output = []
        each = int(sum/n_players)
        for p in range(n_players):
            x = []
            for e in range(each):
                x.append(self.DrawCard())
            output.append(x)

        return output

    def DrawCard(self):
        return self.cards.pop(0)


class City:
    def __init__(self, name, color, id, neighbors):
        self.name = name
        self.color = color
        #disease list goes Blue, Yellow, Black, Red
        self.diseases = [0,0,0,0] #better way than list?
        self.disease_colors = ["blue","yellow","black","red"];
        self.id = int(id)
        self.research_center = False
        self.neighbors = neighbors

        self.outbreaked = False

    def SumDiseaseCubes(self):
        sum = 0
        for k in range(len(self.diseases)):
            sum += self.diseases[k]
        return sum

    def ShowDiseaseStatus(self):
        disease_value = self.SumDiseaseCubes()
        if disease_value > 0:
            print("-----")
            print("City: " + self.name + "(" + str(self.id) +")")
            for c in range(len(self.diseases)):
                print(self.disease_colors[c] + ": " + str(self.diseases[c]))

    def ShowResearchCenterStatus(self):
        if self.research_center:
            print("-----")
            print("City: " + self.name + "(" + str(self.id) + ")")

    def print_info(self):
        #insert some print statements here
        print("City " + self.name + " : " + self.color)

    def CheckIfQuarentined(self, players):
        for p in players:
            if p.role == "Quarantine Specialist":
                if self.id == p.position_id:
                    return True
                else:
                    for n in self.neighbors:
                        if n == p.position_id:
                            return True
                return False
        return False

    def AddDrawnInfection(self, city_list, value, player_list):
        if self.CheckIfQuarentined(player_list):
            return
        if self.color == 'blue':
            self.diseases[0] += value
        elif self.color == 'red':
            self.diseases[3] += value
        elif self.color == 'yellow':
            self.diseases[1] += value
        else:
            self.diseases[2] += value
        self.CheckForOutbreak(city_list, player_list)

    def AddInfectionOfColor(self, color, city_list, player_list):
        if self.CheckIfQuarentined(player_list):
            return
        if color == 'blue':
            self.diseases[0] += 1
        elif color == 'yellow':
            self.diseases[1] += 1
        elif color == 'black':
            self.diseases[2] += 1
        elif color == 'red':
            self.diseases[3] += 1
        self.CheckForOutbreak(city_list, player_list)

    def CheckForOutbreak(self, city_list, player_list):
        if self.outbreaked:
            return
        if self.CheckIfQuarentined(player_list):
            return

        if self.diseases[0] > 3:
            self.diseases[0] = 3
            GenerateOutBreak(self,'blue', city_list)
        elif self.diseases[1] > 3:
            self.diseases[1] = 3
            GenerateOutBreak(self, 'yellow', city_list)
        elif self.diseases[2] > 3:
            self.diseases[2] = 3
            GenerateOutBreak(self, 'black', city_list)
        elif self.diseases[3] > 3:
            self.diseases[3] = 3
            GenerateOutBreak(self, 'red', city_list)

    def GenerateOutBreak(self, color, city_list, player_list):
        self.outbreaked = True
        for n in self.neighbors:
            city_list[n].AddInfectionOfColor(self, color, city_list, player_list)


class PlayerCard:
    def __init__(self, type, name, id):
        self.type = type
        self.name = name
        self.id = id - 1

    def PrintCard(self):
        print("PlayerCard:" + self.type + " - " + self.name)

def CheckForOutbreaks(city_list):
    sum = 0
    for city in city_list:
        if city.outbreaked:
            sum += 1
            city.outbreaked = False

def ShuffleDeck(deck):
    random.shuffle(deck)
    return deck

def SliceDeck(input, size):
    input_size = len(input)
    slice_size = int(input_size / size)
    remain = input_size % size
    result = []
    #iterator = iter(input)
    for i in range(size):
        result.append([])
        for j in range(slice_size):
            result[i].append(input.pop(0))
        if remain:
            result[i].append(input.pop(0))
            remain -= 1
    return result

def SpawnEpidemic(infected_discard, infection_cards, epidemics_occured, city_list, players):
    epidemics_occured += 1
    infection_options = [2,2,2,3,3,4,4]
    infection_rate = infection_options[epidemics_occured]
    bottom_card = infection_cards.pop(-1)
    city_list[bottom_card.id].AddDrawnInfection(city_list,3,players)
    infected_discard.append(bottom_card)
    #reshuffle discard
    infected_discard = ShuffleDeck(infected_discard)
    #stick back on top
    #need to return basically everything?
    return infected_discard.extend(infection_cards)


if __name__ == "__main__" :
    #main area
    city_list = []
    #Step 1: import all the cities from csv
    fn = 'pandemic_cities.csv'
    with open(fn, newline='') as csvfile:
        cityreader = csv.reader(csvfile)
        #todo insert try/catch
        for row in cityreader:
            n = row[3:len(row)]
            city_list.append(City(row[1],row[2],row[0],n))
        #print(row[1])

    #Step 2: construct the graph
    map = Graph(len(city_list))
    city_id_to_name = {}
    city_name_to_id = {}
    for c in city_list:
        # create a dictionary of the city ID to name and a dictionary of name to ID
        real_id = int(c.id)-1
        city_id_to_name[real_id] = c.name
        city_name_to_id[c.name] = real_id
        for d in c.neighbors:
            map.AddEdge(real_id,int(d)-1)

    print("adjaceny list for storing graph")
    #map.Display_AdjList()

    #Initialize Game
    role_deck = ['Medic','Researcher','Operations Expert','Dispatcher','Quarantine Specialist','Scientist','Contingency Planner']
    roles_shuffled = ShuffleDeck(role_deck)
    print(roles_shuffled)
    city_cards = []
    for city in city_list:
        city_cards.append(PlayerCard('city',city.name,int(city.id)))


    infection_cards = city_cards
    infection_cards = ShuffleDeck(infection_cards)

    player_cards = PlayerCardDeck(city_cards)
    player_card_discard = []
    infection_discard = []
    player_list = []

    #Set initial infections -> clean this section up and make it its own function to initialize
    for k in range(9):
        print(city_list[infection_cards[k].id].name)
    #set of 3s
    city_list[infection_cards[0].id].AddDrawnInfection(city_list, 3, player_list)
    city_list[infection_cards[1].id].AddDrawnInfection(city_list, 3, player_list)
    city_list[infection_cards[2].id].AddDrawnInfection(city_list, 3, player_list)
    #set of 2s
    city_list[infection_cards[3].id].AddDrawnInfection(city_list, 2, player_list)
    city_list[infection_cards[4].id].AddDrawnInfection(city_list, 2, player_list)
    city_list[infection_cards[5].id].AddDrawnInfection(city_list, 2, player_list)
    #set of 1s
    city_list[infection_cards[6].id].AddDrawnInfection(city_list, 1, player_list)
    city_list[infection_cards[7].id].AddDrawnInfection(city_list, 1, player_list)
    city_list[infection_cards[8].id].AddDrawnInfection(city_list, 1, player_list)
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
    player_list.append(Players.Player(roles_shuffled[0], "Kevin", 0))
    player_list.append(Players.Player(roles_shuffled[2], "Megan", 1))
    player_list.append(Players.Player(roles_shuffled[1], "Phil", 2))
    player_list.append(Players.Player(roles_shuffled[3], "Jesse", 3))

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
        p.ShowActionOptions(city_list, map, player_list)
    print("====================")
    #--------
    #Print a demo players options

    #Example Round
    #Player does action
    #player draws 2 cards
    #player draws 2 infections
    #player increments outbreak counter