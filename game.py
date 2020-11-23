import csv
from copy import deepcopy

from player import Player
from city import City
from cards import PlayerCard, PlayerCardDeck, ShuffleDeck
from actions import check_action, perform_action, Share, Clean, Cure, Build, DiscardMove, FreeMove


def import_cities(filename):
    city_list = []
    with open(filename) as csvfile:
        cityreader = csv.reader(csvfile)
        # TODO: wrap in try/catch
        for row in cityreader:
            neighbors = [int(n) for n in row[3:]]
            ID, name, color = int(row[0]), row[1], row[2]
            city_list.append(City(ID, name, color, neighbors))

    return city_list


class Game:
    def __init__(self, n_players, difficulty, AI_Decider):
        self.cities = []
        self.city_list = {}
        self.roles = []
        self.player_cards = []
        self.player_discard = []
        self.infection_cards = []
        self.infection_discard = []
        self.infection_cards_restack = [] #a subset of infection cards that track which cards are back on top that were in the discard

        self.round_number = 0
        self.turn_number = 0

        self.cured_diseases = {
            "blue": False,
            "yellow": False,
            "black": False,
            "red": False
        }

        #set initial infection rate
        self.game_lost = False
        self.game_win = False
        self.occurred_epidemics = 0
        self.infection_rate_options = [2,2,2,3,3,4,4]
        self.outbreak_number = 0 #initialize to 0

        self.AI = AI_Decider
        #Add two data trackers
        self.starting_num_of_player_cards = 48+5

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

    @property
    def infection_rate(self):
        return self.infection_rate_options[self.occurred_epidemics]

    def initialize_game(self):
        self.cities = import_cities("pandemic_cities.csv") #need to grab the correct reference
        for city in self.cities:
            self.city_list[city.name] = city
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
        #Check for outbreaks
        self.check_for_outbreaks()

    def play(self):
        # Main game loop
        while self.check_win() is None:
            self.update()

        if self.check_win():
            print("DR. FAUCI HAS WON! on turn " + str(self.turn_number))
        else:
            print("CORONAVIRUS HAS WON! on turn " + str(self.turn_number))

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
            infect.has_been_drawn = True
            self.cities[infect.ID].AddDrawnInfection(self.cities,1,self.players)
            self.infection_discard.append(infect)
            #pull out restack cards if they exist
            if len(self.infection_cards_restack) > 0:
                self.infection_cards.restack.pop(0)

    def spawn_epidemic(self):
        #Part 1: upgrade infection rate
        self.occurred_epidemics += 1
        #Part 2: Cause Infection
        bottom_card = self.infection_cards.pop(-1)
        bottom_card.has_been_drawn = True
        self.cities[bottom_card.ID].AddDrawnInfection(self.cities,3,self.players)
        self.infection_discard.append(bottom_card)
        #Part 3: reshuffle and place on top
        ShuffleDeck(self.infection_discard)
        #update our local tracker of which ones have been drawn and are back on top
        self.infection_cards_restack.extend(self.infection_discard)
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
        print("Number of player cards in generate cards " + str(self.player_cards.remaining_cards()) + " == " + '53')

    def spawn_infection(self):
        for k in range(3):
            for i in range(3):
                self.cities[self.infection_cards[0].ID].AddDrawnInfection(self.cities,3-k,self.players)
                cardref = self.infection_cards.pop(0)
                cardref.has_been_drawn = True
                self.infection_discard.append(cardref)

    def spawn_characters(self):
        random_names = ["Kevin","Phil","Megan","Jessica"];
        for k in range(self.number_of_players):
            self.players.append(Player(self.roles[k],random_names[k],k))
        #Draw cards for the players
        start_cards = self.player_cards.DrawPlayerStartingCards(self.number_of_players)
        for c, p in enumerate(self.players):
            for k in range(len(start_cards[c])):
                p.AddCard(start_cards[c][k])

    def finalize(self):
        self.player_cards.AddEpidemicCards(self.num_of_epidemics)
        self.cities[0].research_center = True
        #this number tracks remaining cards disregarding turn 0 draw
        self.starting_num_of_player_cards = self.player_cards.remaining_cards()

    def check_for_outbreaks(self):
        total = 0
        for city in self.cities:
            if city.outbreaked:
                total += 1
                city.outbreaked = False
        self.outbreak_number += total

    def check_cube_limit(self):
        """
        return: True if all of the disease cubes for any color have been placed
        """

        sum_blue = 0
        sum_red = 0
        sum_yellow = 0
        sum_black = 0
        for city in self.cities:
            sum_blue += city.disease['blue']
            sum_black += city.disease['black']
            sum_yellow += city.disease['yellow']
            sum_red += city.disease['red]']
        if sum_blue > 24 or sum_red > 24 or sum_yellow > 24 or sum_black > 24:
            return True
        else:
            return False

    def check_win(self):
        """
        A loss occurs if any of the following occurs:
            - 8 outbreaks
            - more than 24 disease cubes of one color
            - no cards left

        A win occurs if all four diseases are cured
        """
        if self.outbreak_number >= 8 or self.check_cube_limit():
            return False
        #no cards left is checked when you draw 2 new cards for player

        #all four diseases cured
        if all(self.cured_diseases.values()):
            return True

        return None

    def share_card(self, playerDst, playerSrc, card_index):
        playerDst.card_list.append(playerSrc.card_list.pop(card_index))

    def get_city_by_name(self,name):
        return self.city_list[name]