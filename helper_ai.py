from game import Game
from cards import PlayerCardDeck, PlayerCard


def calculate_uniform_probability_of_card_draw(num_of_cards):
    return 1/num_of_cards

def calculate_chance_of_epidemic(game):
    #Do we cast this as int or round to ceiling?
    print("Epidemic " + str(game.num_of_epidemics) + "#")
    print("Starting Cards " + str(game.starting_num_of_player_cards) + "#")
    split_size = float(game.starting_num_of_player_cards) / game.num_of_epidemics
    print("split size is " + str(split_size))
    cards_left = game.player_cards.remaining_cards()
    cards_burnt = game.starting_num_of_player_cards - cards_left
    #now calculate how many epidemic splits have we gone through
    rem = split_size - cards_burnt % split_size
    print("Remainder Value " + str(rem))
    expected_epidemics = float(cards_burnt / split_size) + 1
    print("Expected Epidemics " + str(expected_epidemics))
    if game.occurred_epidemics >= expected_epidemics:
        return 0
    else:
        #only is ever 2 cards from player side
        a = calculate_uniform_probability_of_card_draw(rem)
        b = calculate_uniform_probability_of_card_draw(rem-1)
        return a + b

def calculate_drawing_infection_city_card(game, city):
    p_epidemic = calculate_chance_of_epidemic(game)
    print("probability of drawing epidemic is " + str(p_epidemic))
    if check_if_in_discard(game,city.name):
        p_card = 0
        for r in range(game.infection_rate):
            p_card += calculate_uniform_probability_of_card_draw(len(game.infection_discard) + 1 - r)
        return p_card * p_epidemic
    else:
        p__not_epidemic = 1 - p_epidemic
        if check_if_has_been_drawn(game,city.name):
            p_card = 0
            for r in range(game.infection_rate):
                p_card += calculate_uniform_probability_of_card_draw(len(game.infection_cards_restack) - r)
            return p__not_epidemic * p_card
        else:
            if len(game.infection_cards_restack) > 0:
                return 0
            else:
                p_card = 0
                for r in range(game.infection_rate):
                    p_card += calculate_uniform_probability_of_card_draw(len(game.infection_cards) - r)
                return p_card * p__not_epidemic + calculate_drawing_epidemic_infection_city_card(game,city)

def check_if_in_discard(game, city_name):
    in_discard = False
    for discard in game.infection_discard:
        if discard.name == city_name:
            in_discard = True
            break
    return in_discard

def check_if_has_been_drawn(game, city_name):
    #only checks the main draw deck
    for card in game.infection_cards:
        if card.name == city_name:
            return card.has_been_drawn
    return False

def calculate_drawing_epidemic_infection_city_card(game, city):
    p_epidemic = calculate_chance_of_epidemic(game)
    #check if its in discard
    if check_if_in_discard(game,city.name) or check_if_has_been_drawn(game,city.name):
        #it can't be drawn from bottom of deck
        return 0
    else:
        #assume uniform distribution for now
        p_card = calculate_uniform_probability_of_card_draw(len(game.infection_cards))
        return p_epidemic * p_card

def calculate_outbreak_in_city(game, city):
    #for now assume only 1 turn and no mixed color outbreaks;
    if city.disesase[city.color] == 3:
        p_draw = calculate_drawing_infection_city_card(game, city)
        return p_draw
    elif city.disesase[city.color] > 1:
        p_draw = calculate_drawing_epidemic_infection_city_card(game,city)
        return p_draw
    else:
        #calculate the probability of drawing epidemic and then redrawing that card
        p_epidemic = calculate_drawing_epidemic_infection_city_card(game, city)
        p_draw = 0
        for x in range(game.infection_rate):
            p_draw += calculate_uniform_probability_of_card_draw(len(game.infection_discard)+1+x)
        return p_epidemic * p_draw


def calculate_probability_of_outbreak(game):
    #calculate the likelihood for each city
    # TODO! add in the other non-color happenstances
    p_x = []
    total = 0
    for city in game.cities:
        p = calculate_outbreak_in_city(game,city)
        total += p
        p_x.append(p)
        print(city.name + " having an outbreak is " + str(p))
    return total