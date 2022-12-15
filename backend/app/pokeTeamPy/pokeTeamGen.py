from utils import *

class PokeTeamGen :
    def __init__(self, format_data_url, pokedex_data_url, moves_data_url, useful_data_url):
        # Load format and pokedex data
        self.format_data = load_json(format_data_url)
        self.pokedex_data = load_json(pokedex_data_url)
        self.moves_data = load_json(moves_data_url)
        self.useful_data = load_json(useful_data_url)

        self.team_members = [TeamMember(), TeamMember(), TeamMember(), TeamMember(), TeamMember(), TeamMember()]
        self.team_size = len(self.team_members)

    def look_for_good_next_mate(self):
        """
        Look for the best next mate to add to the team
        :return: The name of the best next mate
        """
        teammates_dict = {}
        for i in range(0, self.team_size):
            if self.team_members[i].data != None:
                for j in range(0, len(self.team_members[i].data.teammates)):

                    # Get name of mate
                    name_curr_mate = self.team_members[i].data.teammates[j][0]

                    # Check if mate name is not already in the team members
                    already_in_team = False
                    for k in range(0, self.team_size):
                        if name_curr_mate.lower() == self.team_members[k].name.lower():
                            already_in_team = True
                    # Increase the score of the mate if it is not already in the team

                    if name_curr_mate not in teammates_dict  and already_in_team == False:
                        teammates_dict[name_curr_mate] = 1 / (j + 1)
                    elif already_in_team == False:
                        teammates_dict[name_curr_mate] += 1 / (j + 1)

        # Sort the dict by score
        sorted_teammates = sorted(teammates_dict.items(), key=lambda item: -item[1])
        return sorted_teammates

    def look_for_good_counters(self):
        """
        Look for the best counters to the team
        :return: The name of the best counter
        """
        teammcounters_dict = {}
        for i in range(0, self.team_size):
            if self.team_members[i].data != None:
                if self.team_members[i].data.checks_and_counters <= 0:
                    break
                for j in range(0, len(self.team_members[i].data.checks_and_counters)):
                    # Get name of counter
                    name_curr_counter = self.team_members[i].data.checks_and_counters[j][0]
                    # Increase the score of the counter
                    if name_curr_counter not in teammcounters_dict:
                        teammcounters_dict[name_curr_counter] = 1 / (j + 1)
                    else:
                        teammcounters_dict[name_curr_counter] += 1 / (j + 1)

        # Sort the dict by score
        sorted_counters = sorted(teammcounters_dict.items(), key=lambda item: -item[1])
        return sorted_counters

    def complete_team(self, random_variation=False, nb_pkm_max=6):
        """
        Complete the team with the best next mates
        :param random_variation: If true, the next mates will be chosen randomly among the best next mates
        :param nb_pkm_max: The maximum number of pokemon in the team
        :return: None
        """
        for i in range(0, self.team_size):
            # If the pokemon in this slot is not defined
            if self.team_members[i].data == None:
                # look for the best next pokemon for the team
                sorted_teammates = self.look_for_good_next_mate()

                if (random_variation):
                    j = random.randint(0, min(3, len(sorted_teammates) - 1))
                    next_mate_name = sorted_teammates[j][0]
                else:
                    next_mate_name = sorted_teammates[0][0]
                # add the member to the team
                self.set_pokemon_at_index_in_team(next_mate_name, i)

    def set_pokemon_at_index_in_team(self, pokemon_name, index):
        if self._is_valid_pokemon_in_format(pokemon_name):

            self.team_members[index].name = pokemon_name
            self.team_members[index].data = PokemonData(self.format_data, self.pokedex_data, pokemon_name)
            self.team_members[index].desc = self.create_pokemon_set_from_data(self.team_members[index].data)
        else:
            print("[ERROR] Pokemon not in format")