class Player:
    def __init__(self, role, name, ID):
        self.role = role
        self.ID = ID
        self.name = name

        self.position_id = 0
        self.card_list = []
        self.stored_card = None

    def ShowCharacter(self, city_list):
        print("----------")
        print(self.name + " is the " + self.role + " and is in " + city_list[self.position_id].name)
        self.ShowHand()

    def ShowHand(self):
        for c in self.card_list:
            c.PrintCard()

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

    def ShowActionOptions(self, city_list, world_map, players, player_discard):
        print("Showcasing all actions for " + self.name)
        #ferry action
        ferry_opts = self.FerryActionChoices(world_map)
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
        sum = 0
        for card in self.card_list:
            if card.type == 'city':
                if cities[card.ID].color == color:
                    sum += 1
        return sum

    def FerryActionChoices(self, map):
        nid = map.GetNeighbors(self.position_id)
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
                if card.type == 'city':
                    return True
        else:
            for card in self.card_list:
                if card.type == 'city':
                    if card.ID == self.position_id:
                        return True
        return False

    def DirectFlightChoices(self):
        targets = []
        for card in self.card_list:
            if card.type == 'city' and card.ID != self.position_id:
                targets.append(card.ID)
        return targets

    def BuildResearchStationChoice(self, cities):
        if not cities[self.position_id].research_center:
            if self.role == 'Operations Expert':
                return True
            else:
                for card in self.card_list:
                    if card.type == 'city':
                        if card.ID == self.position_id:
                            return True
        return False

    def TreatDiseaseChoices(self, cities):
        dcubes = cities[self.position_id].diseases
        sum = 0
        for dc in dcubes:
            sum += int(dc)
        #right now we are returning the number of available actions;
        return sum

    def CureDiseaseChoice(self, cities):
        results = [False, False, False, False]
        value = 4
        if self.role == 'Scientist':
            value = 3
        if cities[self.position_id].research_center:
            bc = self.GetNumberOfCardsOfColor(cities,'blue')
            yc = self.GetNumberOfCardsOfColor(cities, 'yellow')
            kc = self.GetNumberOfCardsOfColor(cities, 'black')
            rc = self.GetNumberOfCardsOfColor(cities, 'red')
            if bc > value:
                results[0] = True
            if yc > value:
                results[1] = True
            if kc > value:
                results[2] = True
            if rc > value:
                results[3] = True
        return results

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
                    if c.type == 'city':
                        return True
            else:
                for c in friend.card_list:
                    if c.ID == friend.position_id:
                        return True
            if self.role == 'Researcher':
                for c in self.card_list:
                    if c.type == 'city':
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
            if card.type == 'event':
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
                    if p.stored_card.type == 'Forecast':
                        return True
            for c in p.card_list:
                if c.type == 'event':
                    if c.name == 'Forecast':
                        return True
        return False

    def AirliftChoice(self,player_list):
        for p in player_list:
            if p.role == 'Contingency Planner':
                if len(p.stored_card) > 0:
                    if p.stored_card.type == 'Airlift':
                        return True
            for c in p.card_list:
                if c.type == 'event':
                    if c.name == 'Airlift':
                        return True
        return False

    def QuietNightChoice(self,player_list):
        for p in player_list:
            if p.role == 'Contingency Planner':
                if len(p.stored_card) > 0:
                    if p.stored_card.type == 'Quiet Night':
                        return True
            for c in p.card_list:
                if c.type == 'event':
                    if c.name == 'Quiet Night':
                        return True
        return False

    def GovernmentGrantChoice(self,player_list):
        for p in player_list:
            if p.role == 'Contingency Planner':
                if len(p.stored_card) > 0:
                    if p.stored_card.type == 'Government Grant':
                        return True
            for c in p.card_list:
                if c.type == 'event':
                    if c.name == 'Government Grant':
                        return True
        return False

    def ResilientPopChoice(self,player_list):
        for p in player_list:
            if p.role == 'Contingency Planner':
                if len(p.stored_card) > 0:
                    if p.stored_card.type == 'Resilient Population':
                        return True
            for c in p.card_list:
                if c.type == 'event':
                    if c.name == 'Resilient Population':
                        return True
        return False

    def AddTwoCards(self, card_A, card_B):
        self.card_list.append(card_A)
        self.card_list.append(card_B)

    def AddCard(self, card):
        self.card_list.append(card)
