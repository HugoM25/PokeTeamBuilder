from .teamMember import TeamMember
import random 

class TeamBuilder:
    def __init__(self, team=None, tier="", db_handler=None):
        self.team_size = 6
        if team is None :
            self.team = [TeamMember() for _ in range(self.team_size)]
        else :
            self.team = [TeamMember(name=member["name"], locked=member["isLocked"]) for member in team]

        self.tier = tier
        self.db_handler = db_handler

    def set_pokemon_at_index(self, index, pokemon):
        '''
        Set the pokemon at the given index
        @param index: The index of the pokemon to set
        @param pokemon: The pokemon to set
        '''
        self.team[index] = pokemon            
    
    def is_pokemon_in_team(self, pokemon) -> bool:
        '''
        Check if the given pokemon is in the team
        @param pokemon_name: The name of the pokemon to look for
        @return: True if the pokemon is in the team, False otherwise
        '''
        for pkm in self.team :
            if pkm.name == pokemon.name :
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
        pkm = TeamMember()
        #Get random pkm name 

        names = db_handler.get_pokemons_in_tier(tier)
        pkm.name = names[random.randint(0, len(names)-1)]
        pkm.image_url = "https://play.pokemonshowdown.com/sprites/ani/" + pkm.name + ".gif"
        return pkm 
    
    def find_next_mate_BFS(self, curr_mates_list, names_futur_mates) :
        '''
        Complete the team with pokemon from the given tier using BFS approach
        @param curr_mates_list: The list of the current mates
        @param names_futur_mates: The list of the names of the futur mates
        @return: The new member and the new list of the names of the futur mates
        '''
        i = 0
        while i < len(names_futur_mates) :
            next_mate = TeamMember(names_futur_mates[i])
            if not self.is_pokemon_in_team(next_mate) :
                curr_mates_list.append(next_mate)
                new_mates_list = curr_mates_list
                names_futur_mates.extend(self.db_handler.find_pkms_linked_to(next_mate.name, self.tier))
                return next_mate, new_mates_list, names_futur_mates
            i+=1

        #Only happens if all the futur mates are already in the team
        return None, names_futur_mates
    
    def find_next_mate_DFS(self, curr_mates_list, names_futur_mates) :
        '''
        Complete the team with pokemon from the given tier using DFS approach
        @param curr_mates_list: The list of the current mates
        @param names_futur_mates: The list of the names of the futur mates
        @return: The new member and the new list of the names of the futur mates
        '''
        i = 0
        while i < len(names_futur_mates) :
            next_mate = TeamMember(names_futur_mates[i])
            if not self.is_pokemon_in_team(next_mate) :
                curr_mates_list.append(next_mate)
                new_mates_list = curr_mates_list
                names_futur_mates = self.db_handler.find_pkms_linked_to(next_mate.name, self.tier)
                return next_mate, new_mates_list, names_futur_mates
            i+=1

        #Only happens if all the futur mates are already in the team
        return None, names_futur_mates
            
    def complete_team(self, method="BFS"):
        '''
        Complete the team with pokemon from the given tier
        @param db_handler: The database handler to use
        @param tier: The tier to use
        @param method: The method to use to look for the next pokemon : BFS | DFS | RANDOM | COMMON
        '''

        #Use one of the methods to complete the team
        #Currently only BFS is implemented
        #Get the names of the pokemons in the team
        print(self.team)
        mates_list = [] 
        for member in self.team :
            if member.name != "" and member.locked == True :
                mates_list.append(member)
        print(mates_list)

        #Add random pokemon to start the team if it is empty 
        if len(mates_list) < 1 :
            new_pokemon = self.get_random_pokemon_in_format(self.db_handler, self.tier)
            self.set_pokemon_at_index(0, new_pokemon)
            mates_list.append(new_pokemon)
        #Not recommended
        if method == "BFS" :
            next_mates_names = self.db_handler.find_pkms_linked_to(mates_list[0].name, self.tier)
            j = 0
            while j < len(self.team) :
                if self.team[j].name == "" or not self.team[j].locked :
                    self.team[j], mates_list, next_mates_names = self.find_next_mate_BFS(mates_list, next_mates_names)
                j+=1
        #Not recommended
        elif method == "DFS" :
            next_mates_names = self.db_handler.find_pkms_linked_to(mates_list[0].name, self.tier)
            j = 0
            while j < len(self.team) :
                if self.team[j].name == "" or not self.team[j].locked :
                    self.team[j], mates_list, next_mates_names = self.find_next_mate_DFS(mates_list, next_mates_names)
                j+=1
        #As you wish
        elif method == "RANDOM" :
            pass 
        #Recommended 
        elif method == "SMART" :
            pass
        else : 
            print("[ERROR] Method not implemented")

        print(self.team)

    def get_team(self) -> list:
        '''
        Get the team
        @return: The team
        '''
        team_data = [pkm.get_data() for pkm in self.team]
        return team_data