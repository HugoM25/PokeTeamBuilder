from .teamElements import TeamMember
from .utils import load_json
import random 

class TeamBuilder:
    def __init__(self, team=None, tier="", db_handler=None):
        self.team_size = 6
        self.settings_data = load_json(r"D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\settings.json")
        if team is None :
            self.team = [TeamMember() for _ in range(self.team_size)]
        else :
            self.team = [TeamMember(name=member["name"], locked=member["isLocked"], settings=self.settings_data) for member in team]

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

        #Get random pkm name 
        names = db_handler.get_pokemons_in_tier(tier)
        name = names[random.randint(0, len(names)-1)]

        pkm = TeamMember(name=name, settings=self.settings_data)
        return pkm 

    def complete_team(self, method="FAST") :

        #Filter the team to get only the locked pokemon
        current_members_names = [] 
        for member in self.team :
            if member.name != "" and member.locked == True :
                current_members_names.append(member.name)

        #If the team is empty, add a random pokemon
        if len(current_members_names) < 1 :
            new_pokemon = self.get_random_pokemon_in_format(self.db_handler, self.tier)
            self.set_pokemon_at_index(0, new_pokemon)
            current_members_names.append(new_pokemon.name)

        #Select pokemon members 
        if method == "FAST" : 
            for i in range(0, self.team_size) : 
                tmp_member = self.team[i]
                if tmp_member.name == "" or not tmp_member.locked :
                    #Find the next best mate
                    next_mate = self.db_handler.get_next_best_mate(current_members_names, self.tier)
                    #Add the pkm to the team
                    current_members_names.append(next_mate)
                    self.set_pokemon_at_index(i,TeamMember(name=next_mate, settings=self.settings_data))
        else : 
            for i in range(0, self.team_size) :
                tmp_member = self.team[i]
                if tmp_member.name == "" or not tmp_member.locked :
                    #Find the next best mate
                    next_mates_list = self.db_handler.get_next_best_mates(current_members_names, self.tier, limit=5)
                    rand_next_mate_index = random.randint(0, len(next_mates_list)-1)

                    #Add the pkm to the team
                    current_members_names.append(next_mates_list[rand_next_mate_index])
                    self.set_pokemon_at_index(i,TeamMember(name=next_mates_list[rand_next_mate_index], settings=self.settings_data))
        
        #Compose the set of every pokemon 
        for i in range(0, self.team_size) :
            tmp_member = self.team[i]
            tmp_member.compose_set(self.db_handler, tier_name=self.tier)


    def get_team(self) -> list:
        '''
        Get the team
        @return: The team
        '''
        team_data = [pkm.get_data() for pkm in self.team]
        return team_data