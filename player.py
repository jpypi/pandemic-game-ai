class Player:
    def __init__(self, role, name, ID):
        self.role = role
        self.ID = ID
        self.name = name

        self.position_id = 0
        self.card_list = []
        self.stored_card = []

        self.current_action_count = 0

    @property
    def city_cards(self):
        return filter(lambda card: card.kind == "city", self.card_list)

    @property
    def event_cards(self):
        return filter(lambda card: card.kind == "event", self.card_list)

    def HasEventCard(self, card_name):
        for c in p.event_cards:
            if c.name == card_name:
                return True

        return False

    def reset_action_counter(self):
        self.current_action_count = 0

    def increment_action_counter(self):
        self.current_action_count += 1

    def ShowCharacter(self, city_list):
        print("----------")
        print(f"{self.name} is the {self.role} and is in {city_list[self.position_id].name}")
        self.ShowHand()

    def ShowHand(self):
        for c in self.card_list:
            print(c)

    def ShowTeamActions(self, players):
        if self.ForecastChoice(players):
            print("Can use Forecast")
        if self.AirliftChoice(players):
            print("Can use Airlift")
        if self.QuietNightChoice(players):
            print("Can use Quiet Night")
        if self.GovernmentGrantChoice(players):
            print("Can use Government Grant")
        if self.ResilientPopChoice(players):
            print("Can use Resilient Population")

    def ShowActionOptions(self, city_list, players, player_discard):
        print("Showcasing all actions for " + self.name)
        #ferry action
        ferry_opts = self.FerryActionChoices(city_list)
        for k in range(len(ferry_opts)):
            print("Ferry to " + city_list[ferry_opts[k]].name)
        #shuttle action
        value = self.ShuttleActionChoices(city_list)
        if value != 0:
            for k in range(len(value)):
                print("Shuttle to " + city_list[value[k]].name)
        else:
            print("No shuttles available")
        #charter Options
        if self.CharterFlightChoices(city_list):
            print("Can charter a flight anywhere")
        else:
            print("No Charter flight available")
        #Direct Flight Choices
        direct_opts = self.DirectFlightChoices()
        for k in range(len(direct_opts)):
            print("Direct Flight available to " + city_list[direct_opts[k]].name)
        #Build Research Center
        if self.BuildResearchStationChoice(city_list):
            print("Can build Research Station")
        else:
            print("Cannot build Research Station")
        #Treat Diseases Choices
        val = self.TreatDiseaseChoices(city_list)
        print("Can treat " + str(val) + " disease cubes")
        #Cure Disease choices
        cure_opts = self.CureDiseaseChoice(city_list)
        print("Can cure these diseases: " + str(cure_opts))
        #Share Knowledge
        share_opts = self.ShareAllKnowledgeChoice(players)
        print("Can share card with " + str(share_opts))
        #Special Abilities
        if self.ContingencySpecialGrab(player_discard):
            print("Can recover a contingency plan")
        else:
            print("Cannot recover a contingency plan")
        if self.DispatcherControl():
            print("Can move others")
        else:
            print("Not a dispatcher")

    def GetNumberOfCardsOfColor(self, cities, color):
        total = 0
        for card in self.city_cards:
            if cities[card.ID].color == color:
                total += 1
        return total

    def FerryActionChoices(self, cities):
        nid = cities[self.position_id].get_neighbors()
        return nid

    def ShuttleActionChoices(self, cities):
        if cities[self.position_id].research_center:
            mycity = cities[self.position_id]
            targets = []
            for c in cities:
                if c.research_center and c != mycity:
                    targets.append(c)
            return targets
        else:
            return 0

    def CharterFlightChoices(self, cities):
        if self.role == 'Operations Expert' and cities[self.position_id].research_center:
            for card in self.card_list:
                if card.kind == 'city':
                    return True
        else:
            for card in self.city_cards:
                if card.ID == self.position_id:
                        return True
        return False

    def DirectFlightChoices(self):
        targets = []
        for card in self.city_cards:
            if card.ID != self.position_id:
                targets.append(card.ID)
        return targets

    def BuildResearchStationChoice(self, cities):
        if not cities[self.position_id].research_center:
            if self.role == 'Operations Expert':
                return True
            else:
                for card in self.city_cards:
                    if card.ID == self.position_id:
                        return True
        return False

    def TreatDiseaseChoices(self, cities):
        #right now we are returning the number of available actions;
        return sum(cities[self.position_id].diseases.values())

    def CureDiseaseChoice(self, cities):
        curable = []
        required = 4
        if self.role == 'Scientist':
            required = 3

        if cities[self.position_id].research_center:
            for color in ['blue', 'yellow', 'black', 'red']:
                count = self.GetNumberOfCardsOfColor(cities, color)
                if count > required:
                    curable.append(color)

        return curable

    def ShareAllKnowledgeChoice(self, playerlist):
        x = []
        for p in playerlist:
            if p != self:
                x.append(self.ShareKnowledgeChoice(p))
        return x

    def ShareKnowledgeChoice(self, friend):
        if friend.position_id == self.position_id:
            if friend.role == 'Researcher':
                for c in friend.card_list:
                    if c.kind == 'city':
                        return True
            else:
                for c in friend.card_list:
                    if c.ID == friend.position_id:
                        return True
            if self.role == 'Researcher':
                for c in self.card_list:
                    if c.kind == 'city':
                        return True
            else:
                for c in self.card_list:
                    if c.ID == self.position_id:
                        return True

        return False

    def ContingencySpecialGrab(self, player_discard_pile):
        if self.role != 'Contingency Planner':
            return False
        for card in player_discard_pile:
            if card.kind == 'event':
                return True

        return False

    def DispatcherControl(self):
        if self.role == 'Dispatcher':
            return True
        else:
            return False

    def ForecastChoice(self, player_list):
        for p in player_list:
            if p.role == 'Contingency Planner':
                if len(p.stored_card) > 0:
                    if p.stored_card.kind == 'Forecast':
                        return True
            if p.HasEventCard('Forecast'):
                return True

        return False

    def AirliftChoice(self,player_list):
        for p in player_list:
            if p.role == 'Contingency Planner':
                if len(p.stored_card) > 0:
                    if p.stored_card.kind == 'Airlift':
                        return True
            if p.HasEventCard('Airlift'):
                return True

        return False

    def QuietNightChoice(self,player_list):
        for p in player_list:
            if p.role == 'Contingency Planner':
                if len(p.stored_card) > 0:
                    if p.stored_card.kind == 'Quiet Night':
                        return True
            if p.HasEventCard('Quiet Night'):
                return True

        return False

    def GovernmentGrantChoice(self,player_list):
        for p in player_list:
            if p.role == 'Contingency Planner':
                if len(p.stored_card) > 0:
                    if p.stored_card.kind == 'Government Grant':
                        return True
            if p.HasEventCard('Government Grant'):
                return True

        return False

    def ResilientPopChoice(self,player_list):
        for p in player_list:
            if p.role == 'Contingency Planner':
                if len(p.stored_card) > 0:
                    if p.stored_card.kind == 'Resilient Population':
                        return True
            if p.HasEventCard('Resilient Population'):
                return True

        return False

    def AddCard(self, card):
        self.card_list.append(card)
