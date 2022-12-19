from .teamMember import TeamMember

class TeamBuilder:
    def __init__(self):
        self.team_size = 6
        self.team = [TeamMember() for _ in range(self.team_size)]
    
    def set_pokemon_at_index(self, index, pokemon):
        '''
        Set the pokemon at the given index
        @param index: The index of the pokemon to set
        @param pokemon: The pokemon to set
        '''
        self.team[index] = pokemon            
    
    def is_pokemon_in_team(self, pokemon_name) -> bool:
        '''
        Check if the given pokemon is in the team
        @param pokemon_name: The name of the pokemon to look for
        @return: True if the pokemon is in the team, False otherwise
        '''
        for pkm in self.team :
            if pkm.name == pokemon_name :
                return True
        return False

    def is_team_empty(self) -> bool:
        '''
        Check if the team is empty
        @return: True if the team is empty, False otherwise
        '''
        for pkm in self.team :
            if pkm.name != "" :
                return False
        return True

    def get_random_pokemon_in_format(self, db_handler, tier) -> TeamMember:
        '''
        Get a random pokemon in the given format
        @param db_handler: The database handler to use
        @param tier: The tier to use
        @return: The random pokemon
        '''
        pass

    def complete_team(self, db_handler, tier, method="BFS"):
        '''
        Complete the team with pokemon from the given tier
        @param db_handler: The database handler to use
        @param tier: The tier to use
        @param method: The method to use to look for the next pokemon : BFS | DFS | RANDOM | COMMON
        '''
        #Add random pokemon to start the team if it is empty 
        if self.is_team_empty :
            new_pokemon = self.get_random_pokemon_in_format(db_handler, tier)
            self.set_pokemon_at_index(0, new_pokemon)

        #Use one of the methods to complete the team
        #Currently only BFS is implemented
        if method == "BFS" :
            #Get the pokemons with the most links to the first pokemon
            next_mates_names = db_handler.find_pkms_linked_to(self.team[0].name, tier)
            #Add the fives first pokemons to the team
            i = 0
            j = 0
            while j < self.team_size :
                #If the pokemon is not already in the team, add it
                if not self.is_pokemon_in_team(next_mates_names[i]) :
                    self.set_pokemon_at_index(i, TeamMember(next_mates_names[i]))
                    j += 1
                i += 1

    def get_team(self) -> list:
        '''
        Get the team
        @return: The team
        '''
        team_data = [pkm.get_data() for pkm in self.team]
        return team_data