from player import Player
from city import City

class IAction:
    def __init__(self, kind):
        self.kind = kind
        #probably not needed anymore

class FreeMove(IAction):
    def __init__(self, destination, method):
        IAction.__init__('FreeMove')
        self.dst = destination
        self.type = method

    def check(self, player):
        pass

    def perform(self, player, game):
        player.position_id = self.dst
        player.increment_action_counter()

class DiscardMove(IAction):
    def __init__(self, destination, method, discard_card_index):
        IAction.__init__('DiscardMove')
        self.dst = destination
        self.type = method
        self.discard = discard_card_index

    def check(self, player):
        pass

    def perform(self, player, game):
        player.position_id = self.dst
        game.discard_playercard(player, self.discard)
        player.increment_action_counter()

class Build(IAction):
    def __init__(self, discard_card_index, city_index):
        IAction.__init__('Build')
        self.city = city_index
        self.discard = discard_card_index

    def check(self, player):
        pass

    def perform(self, player, game):
        game.cities[self.city].research_center = True
        game.discard_playercard(player,self.discard)
        player.increment_action_counter()

class Cure(IAction):
    def __init__(self, discards, color):
        IAction.__init__('Cure')
        self.discards = discards
        self.cure_color = color

    def check(self, player):
        pass

    def perform(self, player, game):
        game.add_cure(self.cure_color)
        for d in self.discards:
            game.discard_playercard(player, d)
        player.increment_action_counter()

class Clean(IAction):
    def __init__(self, city_index, amount, color):
        IAction.__init__('Clean')
        self.city = city_index
        self.amount = amount
        self.color = color

    def check(self, player):
        pass

    def perform(self, player, game):
        game.cities[self.city].clear_disease_cubes(self.amount,self.color)
        player.increment_action_counter()

class Share(IAction):
    def __init__(self, to_player, from_player, card_index):
        IAction.__init__('Share')
        self.dst = to_player
        self.src = from_player
        self.index = card_index

    def check(self, player):
        pass

    def perform(self, player, game):
        game.share_card(self.dst, self.src,self.index)
        player.increment_action_counter()

def check_action(action, player):
    return action.check(player)

def perform_action(action, player, game):
    action.perform(player, game)
