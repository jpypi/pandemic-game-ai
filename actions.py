class Action:
    def __init__(self, kind):
        self.kind = kind

class FreeMove(Action):
    def __init__(self, destination, method):
        Action.__init__('FreeMove')
        self.dst = destination
        self.type = method

class DiscardMove(Action):
    def __init__(self, destintation, method, discard_card_index):
        Action.__init__('DiscardMove')
        self.dst = destination
        self.type = method
        self.discard = discard_card_index

class Build(Action):
    def __init__(self, discard_card_index, city_index):
        Action.__init__('Build')
        self.city = city_index
        self.discard = discard_card_index

class Cure(Action):
    def __init__(self, discards, color):
        Action.__init__('Cure')
        self.discards = discards
        self.cure_color = color

class Clean(Action):
    def __init__(self, city_index, amount):
        Action.__init__('Clean')
        self.city = city_index
        self.amount = amount

class Share(Action):
    def __init__(self, to_player, from_player, card_index):
        Action.__init__('Share')
        self.dst = to_player
        self.src = from_player
        self.index = card_index