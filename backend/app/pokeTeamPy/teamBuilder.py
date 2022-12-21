from .teamMember import TeamMember
import random 

class TeamBuilder:
    def __init__(self, team=None):
        self.team_size = 6
        if team is None :
            self.team = [TeamMember() for _ in range(self.team_size)]
        else :
            self.team = [TeamMember(name=member["name"], locked=member["isLocked"]) for member in team]
    
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

    def complete_team(self, db_handler, tier, method="BFS"):
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
            new_pokemon = self.get_random_pokemon_in_format(db_handler, tier)
            self.set_pokemon_at_index(0, new_pokemon)
            mates_list.append(new_pokemon)

        if method == "BFS" :
            #Get the pokemons with the most links to the first pokemon
            next_mates_names = db_handler.find_pkms_linked_to(mates_list[0].name, tier)
            i = 0
            j = 0

            member = self.team[j]
            next_mate = TeamMember(next_mates_names[i])
            
            while j < len(self.team) and i < len(next_mates_names) :
                #check if next mate name is not already in the team
                if not self.is_pokemon_in_team(next_mate) :
                    #if the pokemon is not defined or not locked, add the next mate
                    if member.name == "" or not member.locked :
                        self.set_pokemon_at_index(j, next_mate)
                        #add the next pokemon's links to the list of next possibles mates
                        next_mates_names.extend(db_handler.find_pkms_linked_to(next_mate.name, tier))
                        
                    #Goes to the next slot in the team
                    member = self.team[j]
                    j+=1
                else :
                    #Goes to the next pokemon in the list of next mates
                    next_mate = TeamMember(next_mates_names[i])
                    i+=1
        
        print(self.team)
                

                    



    def get_team(self) -> list:
        '''
        Get the team
        @return: The team
        '''
        team_data = [pkm.get_data() for pkm in self.team]
        return team_data