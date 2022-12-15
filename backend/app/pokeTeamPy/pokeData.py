class PokemonData() :
    def __init__(self, data_json_showdown, data_json_pokedex, pokemon_name) :

        self.name = pokemon_name

        #Parse data about pokemon from pokedex
        self.data_pokedex = self._load_pokedex_infos(data_json_pokedex, self.name)
        self.types = self._parse_type_(self.data_pokedex)
        self.base_stats = self._parse_base_stats(self.data_pokedex)
        
        #Parse data about pokemon battle infos
        self.data_self = self._load_battle_infos(data_json_showdown, self.name)
        self.moveset = self._parse_moveset(self.data_self)
        self.checks_and_counters = self._parse_checks_and_counters(self.data_self)
        self.teammates = self._parse_teammate(self.data_self)
        self.items = self._parse_items(self.data_self)
        self.spreads = self._parse_spreads(self.data_self)
        self.abilities = self._parse_abilities(self.data_self)


    def __str__(self):
        return self.name + "DATA"

    def show_best_mates(self, nb):
        for i in range(0,nb) :
            print(self.teammates[i][0] + " : " + str(self.teammates[i][1]))

    def _load_pokedex_infos(self, data_json, pokemon_name):
        #Format pokemon name correctly
        pokemon_name_correct = pokemon_name
        pokemon_name_correct = pokemon_name_correct.replace("-", "")
        pokemon_name_correct = pokemon_name_correct.replace(".", "")
        pokemon_name_correct = pokemon_name_correct.replace("'", "")
        pokemon_name_correct = pokemon_name_correct.replace(" ", "")

        return data_json[pokemon_name_correct.lower()]

    def _parse_base_stats(self, data_json):
        dict_base_stats = data_json["baseStats"]
        return dict_base_stats

    def _parse_type_(self, data_json):
        dict_types = data_json["types"]
        return dict_types

    def _load_battle_infos(self, data_json, pokemon_name):
        return data_json['data'][pokemon_name]

    def _parse_checks_and_counters(self,data_json):
        dict_checks_and_counters = sorted(data_json["Checks and Counters"].items(), key=lambda item: -item[1][0])
        return dict_checks_and_counters

    def _parse_moveset(self, data_json):
        dict_moves = sorted(data_json["Moves"].items(), key=lambda item: -item[1])
        return dict_moves

    def _parse_teammate(self, data_json):
        dict_teammates = sorted(data_json["Teammates"].items(), key=lambda item: -item[1])
        return dict_teammates

    def _parse_items(self, data_json):
        dict_items = sorted(data_json["Items"].items(), key=lambda item: -item[1])
        return dict_items

    def _parse_abilities(self, data_json):
        dict_abilities = sorted(data_json["Abilities"].items(), key=lambda item: -item[1])
        return dict_abilities

    def _parse_spreads(self, data_json):
        dict_nature = sorted(data_json["Spreads"].items(), key=lambda item: -item[1])
        return dict_nature