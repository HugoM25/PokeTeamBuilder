from neo4j import GraphDatabase 
import json 
from urllib.request import urlopen
from . import dataBaseUtils as dbu
from .utils import load_json, remove_non_letters, clean_names, spread_to_dict, dict_to_neo4j_style
from .teamElements import MoveDb
import time

class DataBaseHandler:
    def __init__(self):
        self.uri = "bolt://127.0.0.1:7687"
        #development password, will be changed at release
        self.driver = GraphDatabase.driver(self.uri, auth=("neo4j", "j4oen"))

    def clear_mates_links(self):
        """
        Clear the mates links in the database
        """
        with self.driver.session(database="pokedb") as session:
            session.run("MATCH ()-[r:LINK]->() DELETE r")
            session.run("MATCH ()-[r:IN_TIER]->() DELETE r")
        self.driver.close() 
    
    def clear_current_tiers_links(self) :
        '''
        Clear the current tiers links in the database
        '''
        with self.driver.session(database="pokedb") as session:
            #Delete the tiers links
            session.run("MATCH ()-[r:IN_TIER]->() DELETE r")
            #Delete the mates links
            session.run("MATCH ()-[r:LINK]->() DELETE r")
            #Delete the items links
            session.run("MATCH ()-[r:USES]->() DELETE r")
            #Delete the moves links
            session.run("MATCH ()-[r:KNOWS]->() DELETE r")
            #Delete the abilities links
            session.run("MATCH ()-[r:HAS]->() DELETE r")
            #Delete the spreads links and nodes
            session.run("MATCH (s:Spread) DETACH DELETE s")

    def clear_db(self):
        """
        Clear the database
        """
        with self.driver.session(database="pokedb") as session:
            #Remove nodes
            session.run("MATCH (n) DETACH DELETE n")

        self.driver.close()

    def load_pkdex_data_in_db(self, pokedex_data) :
        """
        Load the pokedex data into the database
        param pokedex_data: pokedex data to be loaded
        """
        with self.driver.session(database="pokedb") as session :
            #add constraint to avoid duplicates
            
            #for every pokemon in pkdex data 
            for pkm_key in list(pokedex_data.keys()):
                #Check the isNonStandard field to see if it is a real pokemon
                if pokedex_data[pkm_key].get("isNonstandard") is None or 'CAP' not in pokedex_data[pkm_key]["isNonstandard"] and 'LGPE' not in pokedex_data[pkm_key]["isNonstandard"] and 'Custom' not in pokedex_data[pkm_key]["isNonstandard"]:
                    #Create the pokemon
                    session.execute_write(dbu.query_create_pokemon, pkm_key, pokedex_data[pkm_key]["num"], pokedex_data[pkm_key]["baseStats"], pokedex_data[pkm_key]["heightm"], pokedex_data[pkm_key]["weightkg"])
                    print("added", pkm_key, "number :", pokedex_data[pkm_key]["num"])
    
    def load_moves_data_in_db(self, moves_data): 
        """
        Load the moves data into the database 
        param moves_data: moves data to be loaded
        """
        for move_key in list(moves_data.keys()):
            #Check the isNonStandard field to see if it is a real move
            if moves_data[move_key].get("isNonstandard") is None or 'CAP' not in moves_data[move_key]["isNonstandard"] and 'LGPE' not in moves_data[move_key]["isNonstandard"] and 'Custom' not in moves_data[move_key]["isNonstandard"]:
                #Create the move
                with self.driver.session(database="pokedb") as session :
                    move_tmp = MoveDb(move_key, moves_data[move_key])
                    #Create the node
                    session.execute_write(dbu.query_create_move, move_tmp)
                    #Add a link between the node and the type of the move 
                    session.execute_write(dbu.query_link_move_to_type, move_key, moves_data[move_key]["type"])

    def load_abilities_data_in_db(self, abilities_data) :
        '''
        Load the abilities data into the database
        param abilities_data: abilities data to be loaded
        '''
        with self.driver.session(database="pokedb") as session :
            for ability_key in list(abilities_data.keys()):
                #Create the ability
                if abilities_data[ability_key].get("isNonstandard") is None or 'CAP' not in abilities_data[ability_key]["isNonstandard"] and 'LGPE' not in abilities_data[ability_key]["isNonstandard"] and 'Custom' not in abilities_data[ability_key]["isNonstandard"]:
                    session.execute_write(dbu.query_create_ability, ability_key, abilities_data[ability_key]["name"], abilities_data[ability_key]["num"], abilities_data[ability_key]["rating"])
                    print("added", ability_key)
    
    def load_moves_pkm_in_db(self, pokemon_data, name_pkm, tier) : 
        """
        Load the moves of a pokemon in the database 
        param pokemon: pokemon to be loaded
        """
        with self.driver.session(database="pokedb") as session :
            #for every move of the pokemon
            for move in pokemon_data["Moves"].keys():
                #Create the link between the pokemon and the move
                session.execute_write(dbu.query_link_poke_to_move, name_pkm, move, tier, pokemon_data["Moves"][move])

    def load_types_data_in_db(self, useful_data):
        """
        Load the types data into the database
        param types_data: types data to be loaded
        """
        types_data = useful_data["moveTypesData"]
        with self.driver.session(database="pokedb") as session :
            for type_key in list(types_data.keys()):
                #Create the type
                session.run("CREATE (t:Type {name: $name, color: $color})", name=type_key, color=types_data[type_key]["color"])
                print("added", type_key)
    
    def load_items_data_in_db(self, items_data) :
        '''
        Load the items data into the database
        param items_data: items data to be loaded
        '''
        with self.driver.session(database="pokedb") as session :
            for item_key in list(items_data.keys()):
                #Create the item
                session.execute_write(dbu.query_create_item, item_key, items_data[item_key]["name"], items_data[item_key]["spritenum"], items_data[item_key]["num"])
                print("added", item_key)

    def link_pkm_with_types_and_evo(self, pokedex_data):
        '''
        Link the pokemon with their types and evolution
        param pokedex_data: pokedex data to be loaded
        ''' 
        with self.driver.session(database="pokedb") as session :
            #add constraint to avoid duplicates
            
            #for every pokemon in pkdex data 
            for pkm_key in list(pokedex_data.keys()):
                #Check the isNonStandard field to see if it is a real pokemon
                if pokedex_data[pkm_key].get("isNonstandard") is None or 'CAP' not in pokedex_data[pkm_key]["isNonstandard"] and 'LGPE' not in pokedex_data[pkm_key]["isNonstandard"] and 'Custom' not in pokedex_data[pkm_key]["isNonstandard"]:
                    #Add link to types
                    for type_name in pokedex_data[pkm_key]["types"]:
                        session.execute_write(dbu.query_link_types_pokemon, pkm_key, type_name)
                    #Add link to evolution
                    if pokedex_data[pkm_key].get("evos") is not None:
                            session.execute_write(dbu.query_link_evolution, pkm_key, pokedex_data[pkm_key]["evos"][0])
                    print("added", pkm_key, "number :", pokedex_data[pkm_key]["num"])
    
    def add_tier_data_fast(self, tier_data, tier_name) :
        '''
        Add the tier data to the database
        @param tier_data: tier data to be loaded
        @param tier_name: name of the tier
        '''
        tier_data = tier_data["data"]
        with self.driver.session(database="pokedb") as session :
            with session.begin_transaction() as tx:
                for pkm_key in list(tier_data.keys()):
                    #Link to tier
                    dbu.query_link_to_tier(tx, pkm_key.lower(), tier_name)
                    #Add link to teammates
                    for mate_key in tier_data[pkm_key]["Teammates"]:
                        if self.check_if_link_exists(remove_non_letters(pkm_key.lower()), remove_non_letters(mate_key.lower()), "LINK") :
                            dbu.query_set_value_link_mates(tx, remove_non_letters(pkm_key.lower()), remove_non_letters(mate_key.lower()), tier_name, tier_data[pkm_key]["Teammates"][mate_key])
                        else : 
                            dbu.query_create_link_mates(tx,  remove_non_letters(pkm_key.lower()), remove_non_letters(mate_key.lower()), tier_name, tier_data[pkm_key]["Teammates"][mate_key])
                    
                    #Add link to moves
                    for move_key in tier_data[pkm_key]["Moves"]:
                        if self.check_if_link_exists(remove_non_letters(pkm_key.lower()), remove_non_letters(move_key.lower()), "KNOWS") :
                            dbu.query_link_pkm_to_move(tx, move_key.lower(), tier_data[pkm_key]["Moves"][move_key], pkm_key.lower(), tier_name)
                        else : 
                            pass
                            
                    #Add link to abilities
                    for ability_key in tier_data[pkm_key]["Abilities"]:
                        dbu.query_link_pkm_to_ability(tx, ability_key.lower(), pkm_key.lower(),tier_data[pkm_key]["Abilities"][ability_key], tier_name)
                    #Add link to items 
                    for item_key in tier_data[pkm_key]["Items"]:
                        dbu.query_link_pkm_to_item(tx, item_key.lower(), pkm_key.lower(), tier_data[pkm_key]["Items"][item_key], tier_name)
                    print("added", pkm_key)

    def add_tier_data_godspeed(self, tier_data, tier_name) :
        '''
        Add the tier data to the database
        @param tier_data: tier data to be loaded
        @param tier_name: name of the tier
        '''
        tier_data = tier_data["data"]
        time_st = time.time()
        with self.driver.session(database="pokedb") as session :
            with session.begin_transaction() as tx:
                for pkm_key in list(tier_data.keys()):
                    #Clean the key
                    clean_pkm_key = remove_non_letters(pkm_key.lower())

                    #Link to tier
                    dbu.query_link_to_tier(tx,clean_pkm_key, tier_name, tier_data[pkm_key]["Raw count"])

                    #Add tier infos on pokemon mates                  
                    list_mates_clean = [clean_names(mate_key) for mate_key in tier_data[pkm_key]["Teammates"].keys()]
                    list_mates_values = list(tier_data[pkm_key]["Teammates"].values())
                    dbu.query_set_list_node(tx, clean_pkm_key, list_mates_clean, list_mates_values, "LINK", "Pokemon", "Pokemon", tier_name)

                    #Add tier infos on pokemon moves                 
                    list_moves_clean = [clean_names(move_key) for move_key in tier_data[pkm_key]["Moves"].keys()]
                    list_moves_values = list(tier_data[pkm_key]["Moves"].values())
                    dbu.query_set_list_node(tx, clean_pkm_key, list_moves_clean, list_moves_values, "KNOWS", "Move","Pokemon", tier_name)

                    #Add tier infos on pokemon abilities               
                    list_abilities_clean = [clean_names(ability_key) for ability_key in tier_data[pkm_key]["Abilities"].keys()]
                    list_abilities_values = list(tier_data[pkm_key]["Abilities"].values())
                    dbu.query_set_list_node(tx, clean_pkm_key, list_abilities_clean, list_abilities_values, "HAS", "Ability","Pokemon", tier_name)


                    #Add tier infos on pokemon items
                    list_items_clean = [clean_names(item_key) for item_key in tier_data[pkm_key]["Items"].keys()]
                    list_items_values = list(tier_data[pkm_key]["Items"].values())
                    dbu.query_set_list_node(tx, clean_pkm_key, list_items_clean, list_items_values, "USES", "Item","Pokemon", tier_name)

                    #Add tier infos on pokemon spreads
                    #Unfortunately the longest operation, there is so much data that we only take the first 30 spreads
                    sorted_spreads = sorted(tier_data[pkm_key]["Spreads"].keys()) 
                    nb_spreads_to_extract = min(30, len(sorted_spreads))

                    list_spreads_clean = [ spread_to_dict(sorted_spreads[i]) for i in range(nb_spreads_to_extract)]
                    #Now dict in python are like this { "key": value, "key2": value2, ...} but we want it to be like this {key: value, key2: value2, ...} so we remove the quotes
                    
                    list_spreads_clean = [dict_to_neo4j_style(str(list_spreads_clean[i])) for i in range(nb_spreads_to_extract)]
                    #TO DO remove the number quotes (preventing them from becoming int)
                    list_spreads_values = [tier_data[pkm_key]["Spreads"][sorted_spreads[i]] for i in range(nb_spreads_to_extract)]
                    dbu.query_set_list_spreads(tx, list_spreads_clean, list_spreads_values, clean_pkm_key, tier_name,"HAS_SPREAD")

                    print("added", pkm_key)
                    
        print("Time for tier : ", tier_name, " is : ", time.time() - time_st)

    def get_thing_for_pkm(self, pkm_name, thing_type, relation_type, tier, nb_thing=20) :
        '''
        Get the items for the given pokemon
        @param pkm_name: name of the pokemon
        '''
        with self.driver.session(database="pokedb") as session :
            values = session.run(
            f"""
            MATCH (p:Pokemon)-[r:{relation_type}]-(i:{thing_type})
            WHERE p.name = "{pkm_name}" AND r.{tier} IS NOT NULL
            RETURN i ORDER BY r.{tier} DESC
            LIMIT {nb_thing}
            """
            )
            result = [dict(i) for i in values]
            return result

    def find_pkms_linked_to(self, pkm_name, tier_name, nb_pkms=20):
        '''
        Find the pokemons linked to the given pokemon
        param pkm_name: name of the pokemon
        param tier_name: name of the tier
        param nb_pkms: number of pokemons to return
        '''
        names = []
        #get nb_pkms pokemons linked to the given pokemon and prints them
        with self.driver.session(database="pokedb") as session :
            values = session.run("MATCH (p1:Pokemon)-[r:LINK]->(p2:Pokemon) WHERE p1.name=$pkm_name AND r.name=$tier_name RETURN p2 ORDER BY r.value DESC LIMIT $nb_pkms", pkm_name=pkm_name, tier_name=tier_name, nb_pkms=nb_pkms)
            for value in values:
                names.append(value[0]["name"])
        return names

    def get_pokemons_in_tier(self, tier_name) :
        '''
        Get the pokemons in the given tier
        param tier_name: name of the tier
        '''
        names = []
        with self.driver.session(database="pokedb") as session :
            names_response = session.run("MATCH (p:Pokemon)-[r:IN_TIER]->(t:Tier) WHERE t.name=$tier_name RETURN p.name ORDER BY p.name ", tier_name=tier_name)
            for name in names_response:
                names.append(str(name[0]))
        return names
    
    def get_tiers(self) :
        '''
        Get the tiers
        '''
        tiers = []
        with self.driver.session(database="pokedb") as session :
            tiers_response = session.run("MATCH (t:Tier)-[]-(p:Pokemon) RETURN DISTINCT t.name ORDER BY t.name")
            for tier in tiers_response:
                tiers.append(str(tier[0]))
        return tiers
    
    def check_if_node_exists(self, label, property_name, property_value ):
        '''
        Check if a node exists
        '''
        # Execute the Cypher query
        with self.driver.session(database="pokedb") as session:
            result = session.run(f"MATCH (a:{label} {{{property_name}: '{property_value}'}}) RETURN a")
            # Check if the query returned a record
            if result.single() :
                return True
            else :
                return False
    
    def check_if_link_exists(self, type_node1, type_node2, name_node1, name_node2, link_type):
        '''
        Check if a link exists
        '''
        # Execute the Cypher query
        with self.driver.session(database="pokedb") as session:
            result = session.run(f"MATCH (a:{type_node1})-[r:{link_type}]->(b:{type_node2}) WHERE a.name = '{name_node1}' AND b.name = '{name_node2}' RETURN r")
            # Check if the query returned a record
            if result.single() :
                return True
            else :
                return False
    def find_next_best_mate(self, team) :
        '''
        Finds the next best pokemon to add to a team
        param team: list of pokemon names
        '''
        with self.driver.session(database="pokedb") as session :
            result = session.run(
            "MATCH (p:Pokemon)-[r:LINK]->(m:Pokemon) "
            "WHERE p.name IN $team AND r.name = 'GEN8OU' AND NOT m.name IN $team "
            "WITH m, sum(r.value) as totalMateValue "
            "ORDER BY totalMateValue DESC "
            "LIMIT 1 "
            "RETURN m.name as nextBestMate",
            team=team
        )
            return result.single().value('nextBestMate')

    def get_next_best_mate(self, pkm_team, tier_name) :
        with self.driver.session(database="pokedb") as session : 
            result = session.run(
                f"""
                WITH {pkm_team} as team
                MATCH (p:Pokemon)-[r:LINK]->(m:Pokemon)
                WHERE p.name IN team AND r.{tier_name} IS NOT NULL AND NOT m.name IN team
                WITH m, sum(r.{tier_name}) as totalMateValue
                ORDER BY totalMateValue DESC
                LIMIT 1
                RETURN m.name as nextBestMate
                """
            )
            return result.single().value('nextBestMate')
    
    def get_next_best_mates(self, pkm_team, tier_name, limit=10) :
        with self.driver.session(database="pokedb") as session : 
            result = session.run(
                f"""
                WITH {pkm_team} as team
                MATCH (p:Pokemon)-[r:LINK]->(m:Pokemon)
                WHERE p.name IN team AND r.{tier_name} IS NOT NULL AND NOT m.name IN team
                WITH m, sum(r.{tier_name}) as totalMateValue
                ORDER BY totalMateValue DESC
                LIMIT {limit}
                RETURN m.name as nextBestMates
                """
            )
            return list(result.value('nextBestMates'))

    def get_stats_tier(self, tier): 

        query1 = f"""match (p:Pokemon)-[r:IN_TIER]-(ti:Tier) where ti.name="{tier}" return sum(p.st_hp*r.value)/sum(r.value) as av_hp, sum(p.st_atk*r.value)/sum(r.value) as av_atk,  sum(p.st_def*r.value)/sum(r.value) as av_def,
            sum(p.st_spa*r.value)/sum(r.value) as av_spa, sum(p.st_spd*r.value)/sum(r.value) as av_spd, sum(p.st_spe*r.value)/sum(r.value) as av_spe
            """
        
        query2 = f"""match (ty:Type)-[]-(p:Pokemon), (p)-[r:IN_TIER]-(ti:Tier) where ti.name="{tier}" return ty.name, ty.color, sum(r.value) as nb_pkm order by nb_pkm desc"""

        with self.driver.session(database="pokedb") as session :
            #Get the average stats of the tier
            result = session.run(
                query1
            )
            av_stats = result.single()   
            av_stats = dict(av_stats)       

            #Get the type repartition in the tier
            result = session.run(
                query2
            )
            list_values = result.values()

            type_repartition = {}

            for value in list_values :
                type_repartition[value[0]] = {
                    'color' : value[1],
                    'nb_pkm' : value[2]
                }
            

            final_stats = {
                'average_stats' : av_stats,
                'type_repartition' : type_repartition
            }
            return final_stats

def get_pokemon_names_in_format(format_name: str) -> list:
    """
    Returns a list of all pokemon names in a given format
    """
    data = load_json("D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\gen8ou-0.json")
    pkm_names = list(data['data'].keys())
    return pkm_names

def load_json_url(url):
    '''
    Loads a json file from a url
    '''
    print(url)
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json

def initialize_db():
    db_handler = DataBaseHandler()
    #Load resources
    json_data = load_json(r"D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\pokedex.json")
    useful_data = load_json(r"D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\useful_data.json")
    #Reset db
    db_handler.clear_db()
    #Load the types in the database
    db_handler.load_types_data_in_db(useful_data)
    #Load the pokemons in the database
    db_handler.load_pkdex_data_in_db(json_data)
    #Load the links between pokemons evolutions and types
    db_handler.link_pkm_with_types_and_evo(json_data)
    print("Done")

def update_db():
    import time 
    start_time = time.time()
    db_handler = DataBaseHandler()
    #Remove links mate data 
    db_handler.clear_current_tiers_links()

    #Load every tiers .json files tracked 
    files_tracked = load_json(r"D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\settings.json")

    for tier in files_tracked["tiersTracked"]:
        if db_handler.check_if_node_exists("Tier", "name", tier) == False:
            #Create the tier node
            with db_handler.driver.session() as session:
                session.write_transaction(dbu.create_tier, tier)
        #Add data to db 
        file_name = files_tracked["tiersTracked"][tier]["fileNameShowdown"]
        tier_data = load_json_url("https://www.smogon.com/stats/2022-12/chaos/{}".format(file_name))
        db_handler.add_tier_data_godspeed(tier_data=tier_data, tier_name=tier)
        print("Done for {}".format(tier))

    #Now that tiers are loaded in the db, we can look at some stats for the tiers : 
    

    print("Time taken : {}".format(time.time() - start_time))
    print("Done")
    




if __name__ == "__main__" :
    '''
    When the script running as main, the database is updated with the data from the tiers tracked
    '''
    update_db()


    




