class City:
    def __init__(self, name, color, ID, neighbors):
        self.name = name
        self.color = color
        #disease list goes Blue, Yellow, Black, Red
        self.diseases = [0,0,0,0] #better way than list?
        self.disease_colors = ["blue","yellow","black","red"];
        self.ID = int(ID)
        self.research_center = False
        self.neighbors = neighbors

        self.outbreaked = False

    def SumDiseaseCubes(self):
        sum = 0
        for k in range(len(self.diseases)):
            sum += self.diseases[k]
        return sum

    def ShowDiseaseStatus(self):
        disease_value = self.SumDiseaseCubes()
        if disease_value > 0:
            print("-----")
            print("City: " + self.name + "(" + str(self.ID) +")")
            for c in range(len(self.diseases)):
                print(self.disease_colors[c] + ": " + str(self.diseases[c]))

    def ShowResearchCenterStatus(self):
        if self.research_center:
            print("-----")
            print("City: " + self.name + "(" + str(self.ID) + ")")

    def print_info(self):
        #insert some print statements here
        print("City " + self.name + " : " + self.color)

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
        if self.color == 'blue':
            self.diseases[0] += value
        elif self.color == 'red':
            self.diseases[3] += value
        elif self.color == 'yellow':
            self.diseases[1] += value
        else:
            self.diseases[2] += value
        self.CheckForOutbreak(city_list, player_list)

    def AddInfectionOfColor(self, color, city_list, player_list):
        if self.CheckIfQuarentined(player_list):
            return
        if color == 'blue':
            self.diseases[0] += 1
        elif color == 'yellow':
            self.diseases[1] += 1
        elif color == 'black':
            self.diseases[2] += 1
        elif color == 'red':
            self.diseases[3] += 1
        self.CheckForOutbreak(city_list, player_list)

    def CheckForOutbreak(self, city_list, player_list):
        if self.outbreaked:
            return
        if self.CheckIfQuarentined(player_list):
            return

        if self.diseases[0] > 3:
            self.diseases[0] = 3
            GenerateOutBreak(self,'blue', city_list)
        elif self.diseases[1] > 3:
            self.diseases[1] = 3
            GenerateOutBreak(self, 'yellow', city_list)
        elif self.diseases[2] > 3:
            self.diseases[2] = 3
            GenerateOutBreak(self, 'black', city_list)
        elif self.diseases[3] > 3:
            self.diseases[3] = 3
            GenerateOutBreak(self, 'red', city_list)

    def GenerateOutBreak(self, color, city_list, player_list):
        self.outbreaked = True
        for n in self.neighbors:
            city_list[n].AddInfectionOfColor(self, color, city_list, player_list)
