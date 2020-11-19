import csv

from player import Player
from city import City
from cards import PlayerCard, PlayerCardDeck, ShuffleDeck
from copy import deepcopy
from actions import check_action, perform_action, Share, Clean, Cure, Build, DiscardMove, FreeMove

def import_cities():
    city_list = []
    # Step 1: import all the cities from csv
    fn = 'pandemic_cities.csv'
    with open(fn) as csvfile:
        cityreader = csv.reader(csvfile)
        # todo insert try/catch
        for row in cityreader:
            neighbors = []
            for k in range(3,len(row)):
                neighbors.append(int(row[k]))
            ID, name, color = int(row[0]), row[1], row[2]
            city_list.append(City(ID, name, color, neighbors))
    return city_list


class Game:
    def __init__(self, n_players,difficulty, AI_Decider):
        self.cities = []
        self.roles = []
        self.player_cards = []
        self.player_discard = []
        self.infection_cards = []
        self.infection_discard = []

        self.round_number = 0
        self.turn_number = 0

        self.cured_diseases = {"blue": False, "yellow":False, "black":False, "red":False}

        #set initial infection rate
        self.game_lost = False
        self.game_win = False
        self.occurred_epidemics = 0
        self.infection_rate_options = [2,2,2,3,3,4,4]
        self.infection_rate = self.infection_rate_options[self.occurred_epidemics]
        self.outbreak_number = 0 #initialize to 0

        self.AI = AI_Decider

        #Players
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
        #which player turn:
        playerTurn = self.which_player_turn()
        #Run the AI to make decisions
        if self.AI is not None:
            game_copy = deepcopy(self)
            actions = self.AI.SetActionOptions(playerTurn,game_copy)
        #perform action
        self.do_action(actions,playerTurn)
        #draw cards
        self.draw_playercards(playerTurn)
        #draw infections
        self.draw_infections()
        #reset action counter for next round
        playerTurn.reset_action_counter()
        self.turn_number += 1

    def play(self):
        # TODO: Loop over turns
        #check game state; lose or win
        while not self.game_lost or self.game_win:
            self.update()
        if self.game_lost:
            print("CORONAVIRUS HAS WON! on turn " + str(self.turn_number))
        else:
            print("DR. FAUCI HAS WON! on turn " + str(self.turn_number))

    def do_action(self, list_of_actions, player):
        #list of actions (order dependent) for player
        for act in list_of_actions:
            if check_action(act,player):
                perform_action(act,player,self)

    def which_player_turn(self):
        pi = self.turn_number % self.number_of_players
        return self.players[pi]

    def discard_playercard(self, player, index):
        self.player_discard.append(player.card_list.pop(index))

    def draw_playercards(self, player):
        #draw 2 cards
        if self.player_cards.number_of_cards_left > 2:
            #card 1
            c = self.player_cards.DrawCard()
            if c.kind == 'Epidemic':
                self.spawn_epidemic()
            else:
                player.AddCard(c)
            #card 2
            c = self.player_cards.DrawCard()
            if c.kind == 'Epidemic':
                self.spawn_epidemic()
            else:
                player.AddCard(c)
        else:
            self.game_lost = True
            return

    def draw_infections(self):
        for k in range(self.infection_rate):
            infect = self.infection_cards.pop(0)
            self.cities[infect.ID].AddDrawnInfection(self.cities,1,self.players)
            self.infection_discard.append(infect)

    def spawn_epidemic(self):
        #Part 1: upgrade infection rate
        self.occurred_epidemics += 1
        self.infection_rate = self.infection_rate_options[self.occurred_epidemics]
        #Part 2: Cause Infection
        bottom_card = self.infection_cards.pop(-1)
        self.cities[bottom_card.ID].AddDrawnInfection(self.cities,3,self.players)
        self.infection_discard.append(bottom_card)
        #Part 3: reshuffle and place on top
        ShuffleDeck(self.infection_discard)
        self.infection_cards = self.infection_discard.extend(self.infection_cards)

    def print_game_state(self):
        print("================")
        print("Diseased Cities List")
        for c in self.cities:
            c.ShowDiseaseStatus()
        print("================")
        print("Research Center List")
        for c in self.cities:
            c.ShowResearchCenterStatus()
        print("================")
        print("Players")
        for p in self.players:
            p.ShowCharacter(self.cities)
            p.ShowActionOptions(self.cities,self.players,self.player_discard)
        print("================")

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

    def check_for_outbreaks(self):
        total = 0
        for city in self.cities:
            if city.outbreaked:
                total += 1
                city.outbreaked = False

    def check_for_lose_state(self):
        #8 outbreaks, more than 24 disease cubes of one color, no cards left
        pass

    def check_for_win_state(self):
        #all four diseases cured
        pass

    def share_card(self, playerDst, playerSrc, card_index):
        playerDst.card_list.append(playerSrc.card_list.pop(card_index))
