import random


__all__ = ["PlayerCardDeck", "PlayerCard", "ShuffleDeck", "SliceDeck"]


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
        ShuffleDeck(self.cards)

    def AddEpidemicCards(self, number_of_epidemics):
        sliced_decks = SliceDeck(self.cards, number_of_epidemics)
        temp_deck = []  # reset the player deck now
        for k in sliced_decks:
            k.append(PlayerCard('Epidemic', 'Oh Shit', 1000))
            ShuffleDeck(k)
            # stack back together
            temp_deck.extend(k)
        self.cards = temp_deck

    def DrawPlayerStartingCards(self, n_players):
        if n_players == 3:
            total = 9
        else:
            total = 8

        output = []
        each = int(total / n_players)
        for p in range(n_players):
            output.append([self.DrawCard() for _ in range(each)])

        return output

    def DrawCard(self):
        return self.cards.pop(0)

    def remaining_cards(self):
        return len(self.cards)

class PlayerCard:
    def __init__(self, kind, name, ID):
        self.kind = kind
        self.name = name
        self.ID = ID - 1
        self.has_been_drawn = False

    def __str__(self):
        return f"PlayerCard: {self.kind} - {self.name}"


def ShuffleDeck(deck):
    random.shuffle(deck)


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
