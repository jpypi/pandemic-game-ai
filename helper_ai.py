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
        a = calculate_uniform_probability_of_card_draw(rem)
        b = calculate_uniform_probability_of_card_draw(rem-1)
        return a + b

def calculate_drawing_infection_city_card(game, city_name):
    in_discard = False
    for discard in game.infection_discard:
        if discard.name == city_name:
            in_discard = True
            break
    p_epidemic = calculate_chance_of_epidemic(game)
    print("probability of drawing epidemic is " + str(p_epidemic))
    if in_discard:
        p_card = calculate_uniform_probability_of_card_draw(len(game.infection_discard) + 1)
        p_card2 = calculate_uniform_probability_of_card_draw(len(game.infection_discard))
        return (p_card + p_card2) * p_epidemic
    else:
        p__not_epidemic = 1 - p_epidemic
        #first card
        p_card = calculate_uniform_probability_of_card_draw(len(game.infection_cards))
        #second card
        p_card2 = calculate_uniform_probability_of_card_draw(len(game.infection_cards)-1)
        return (p_card + p_card2) * p__not_epidemic

def calculate_outbreak_in_city(game, city):
    p_draw = calculate_drawing_infection_city_card(game, city.name)


def calculate_probability_of_outbreak(game):
    #calculate the likelihood for each city
    # TODO! add in the other non-color happenstances
    for city in game.cities:
