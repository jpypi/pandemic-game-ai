import csv

from player import Player
from city import City
from cards import PlayerCard, PlayerCardDeck, ShuffleDeck

def import_cities():
    city_list = []
    # Step 1: import all the cities from csv
    fn = 'pandemic_cities.csv'
    with open(fn) as csvfile:
        cityreader = csv.reader(csvfile)
        # todo insert try/catch
        for row in cityreader:
            neighbors = row[3:]
            ID, name, color = int(row[0]), row[1], row[2]
            city_list.append(City(ID, name, color, neighbors))
    return city_list


class Game:
    def __init__(self, n_players,difficulty):
        self.cities = []
        self.roles = []
        self.player_cards = []
        self.player_discard = []
        self.infection_cards = []
        self.infection_discard = []

        self.number_of_players = n_players
        self.players = []
        #set difficulty
        if difficulty == 'easy':
            self.num_of_epidemics = 4
        elif difficulty == 'standard':
            self.num_of_epidemics = 5
        else:
            self.num_of_epidemics = 6

        self.initialize_game()


    def initialize_game(self):
        self.cities = import_cities() #need to grab the correct reference
        self.generate_card_decks()
        self.spawn_infection()
        self.spawn_characters()
        self.finalize()

    def update(self):
        # TODO: Implement a single turn
        pass

    def play(self):
        # TODO: Loop over turns
        pass

    def generate_card_decks(self):
        #role deck
        role_deck = ['Medic',
                     'Researcher',
                     'Operations Expert',
                     'Dispatcher',
                     'Quarantine Specialist',
                     'Scientist',
                     'Contingency Planner']
        ShuffleDeck(role_deck)
        self.roles = role_deck
        #player cards
        city_cards = []
        for city in self.cities:
            city_cards.append(PlayerCard('city', city.name, city.ID))
        self.player_cards = PlayerCardDeck(city_cards) #shuffles internally
        #infection cards
        self.infection_cards = city_cards
        ShuffleDeck(self.infection_cards)

    def spawn_infection(self):
        for k in range(3):
            for i in range(3):
                index = k*3 + i
                self.cities[self.infection_cards[index].ID].AddDrawnInfection(self.cities,3-k,self.players)
                self.infection_discard.append(self.infection_cards.pop(0))

    def spawn_characters(self):
        random_names = ["Kevin","Phil","Megan","Jessica"];
        for k in range(self.number_of_players):
            self.players.append(Player(self.roles[k],random_names[k],k))
        #Draw cards for the players
        start_cards = self.player_cards.DrawPlayerStartingCards(self.number_of_players)
        c = 0
        for p in self.players:
            for k in range(len(start_cards[c])):
                p.AddCard(start_cards[c][k])
            c += 1

    def finalize(self):
        self.player_cards.AddEpidemicCards(self.num_of_epidemics)
        self.cities[0].research_center = True