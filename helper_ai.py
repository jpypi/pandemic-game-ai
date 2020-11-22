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
    print(cards_burnt)
    #now calculate how many epidemic splits have we gone through
    rem = cards_burnt % split_size
    print(rem)
    expected_epidemics = cards_burnt / split_size
    if game.occurred_epidemics >= expected_epidemics:
        return 0
    else:
        return 1/rem

def calculate_drawing_infection_city_card(game, city_name):
    in_discard = False
    for discard in game.infection_discard:
        if discard.name == city_name:
            in_discard = True
            break
    p_epidemic = calculate_chance_of_epidemic(game)
    print(p_epidemic)
    if in_discard:
        p_card = calculate_uniform_probability_of_card_draw(len(game.infection_discard)+1)
        return p_card * p_epidemic
    else:
        p__not_epidemic = 1 - p_epidemic
        p_card = calculate_uniform_probability_of_card_draw(len(game.infection_discard))
        return p_card * p__not_epidemic
