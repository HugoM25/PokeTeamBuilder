class PokeDesc : 
    def __init__(self, name="Missingno", item="None", moveset=None, ability="None", nature="Jovial", evs=None, ivs=None, level=100):
        self.name = name
        self.item = item
        self.ability = ability
        self.nature = nature
        self.level = level
        self.moveset = moveset
        self.evs = evs
        self.ivs = ivs

    def __str__(self) -> str:
        """
        Returns a string representation of the object following the Showdown format as such :
        Name @ Item
        Ability: Ability
        Level: 100
        EVs: 252 HP / 252 Atk / 252 Def / 252 SpA / 252 SpD / 252 Spe
        Nature: Nature
        - Move 1
        - Move 2
        - Move 3
        - Move 4
        """
        str_obj = self.name + " @ " + self.item + "\n"
        str_obj += "Ability: " + self.ability + "\n"
        str_obj += "Level:" + str(self.level) + "\n"
        str_obj += "EVs: {} HP / {} Atk / {} Def / {} SpA / {} SpD / {} Spe\n".format(self.evs[0], self.evs[1], self.evs[2], self.evs[3], self.evs[4], self.evs[5])
        str_obj += self.nature.capitalize() + " Nature\n"
        for move in self.moveset :
            str_obj += "- " + move[0] + "\n"
        return str_obj  
    