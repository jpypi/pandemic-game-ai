class City:
    def __init__(self, ID, name, color, neighbors):
        self.ID = ID
        self.name = name
        self.color = color
        self.diseases = {
            "blue": 0,
            "yellow": 0,
            "black": 0,
            "red": 0
        }
        self.neighbors = neighbors

        self.research_center = False
        self.outbreaked = False

    def ShowDiseaseStatus(self):
        disease_value = sum(self.diseases.values())
        if disease_value > 0:
            print("-----")
            print(f"City: {self.name}({self.ID})")
            for color, value in self.diseases.items():
                print(f"{color}: {value}")

    def ShowResearchCenterStatus(self):
        if self.research_center:
            print("-----")
            print(f"City: {self.name}({self.ID})")

    def PrintInfo(self):
        print(f"City {self.name} : {self.color}")

    def CheckIfQuarentined(self, players):
        for p in players:
            if p.role == "Quarantine Specialist":
                if self.ID == p.position_id:
                    return True
                else:
                    for n in self.neighbors:
                        if n == p.position_id:
                            return True
                return False
        return False

    def AddDrawnInfection(self, city_list, value, player_list):
        if self.CheckIfQuarentined(player_list):
            return
        self.diseases[self.color] += value
        self.CheckForOutbreak(city_list, player_list)

    def AddInfectionOfColor(self, color, city_list, player_list):
        if self.CheckIfQuarentined(player_list):
            return
        self.diseases[color] += 1
        self.CheckForOutbreak(city_list, player_list)

    def CheckForOutbreak(self, city_list, player_list):
        if self.outbreaked or self.CheckIfQuarentined(player_list):
            return

        for color, value in self.diseases.items():
            if value > 3:
                self.diseases[color] = 3
                self.GenerateOutBreak(color, city_list)

    def GenerateOutBreak(self, color, city_list, player_list):
        self.outbreaked = True
        for n in self.neighbors:
            city_list[n].AddInfectionOfColor(self, color, city_list, player_list)

    def get_neighbors(self):
        return self.neighbors

