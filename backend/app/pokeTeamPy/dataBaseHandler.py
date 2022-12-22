from neo4j import GraphDatabase 
import json 
from urllib.request import urlopen


class DataBaseHandler:
    def __init__(self):
        self.uri = "neo4j://localhost:7687"
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
            for pkm_key in list(json_data.keys()):
                #Check the isNonStandard field to see if it is a real pokemon
                if pokedex_data[pkm_key].get("isNonstandard") is None or 'CAP' not in pokedex_data[pkm_key]["isNonstandard"] and 'LGPE' not in pokedex_data[pkm_key]["isNonstandard"] and 'Custom' not in pokedex_data[pkm_key]["isNonstandard"]:
                    #Create the pokemon
                    session.execute_write(create_pokemon, pkm_key, pokedex_data[pkm_key]["num"], pokedex_data[pkm_key]["baseStats"], pokedex_data[pkm_key]["heightm"], pokedex_data[pkm_key]["weightkg"])
                    print("added", pkm_key, "number :", pokedex_data[pkm_key]["num"])
    
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

    def link_pkm_with_types_and_evo(self, pokedex_data):
        '''
        Link the pokemon with their types and evolution
        param pokedex_data: pokedex data to be loaded
        ''' 
        with self.driver.session(database="pokedb") as session :
            #add constraint to avoid duplicates
            
            #for every pokemon in pkdex data 
            for pkm_key in list(json_data.keys()):
                #Check the isNonStandard field to see if it is a real pokemon
                if pokedex_data[pkm_key].get("isNonstandard") is None or 'CAP' not in pokedex_data[pkm_key]["isNonstandard"] and 'LGPE' not in pokedex_data[pkm_key]["isNonstandard"] and 'Custom' not in pokedex_data[pkm_key]["isNonstandard"]:
                    #Add link to types
                    for type_name in pokedex_data[pkm_key]["types"]:
                        session.execute_write(link_types_pokemon, pkm_key, type_name)
                    #Add link to evolution
                    if pokedex_data[pkm_key].get("evos") is not None:
                            session.execute_write(link_evolution, pkm_key, pokedex_data[pkm_key]["evos"][0])
                    print("added", pkm_key, "number :", pokedex_data[pkm_key]["num"])
    
    def add_tier_data(self, tier_data, tier_name):
        '''
        Add the tier data to the database
        param tier_data: tier data to be loaded
        param tier_name: name of the tier
        '''
        tier_data = tier_data["data"]
        with self.driver.session(database="pokedb") as session :
            for pkm_key in list(tier_data.keys()):
                #Link to tier
                session.execute_write(link_to_tier, pkm_key.lower(), tier_name)
                #Add link to teammates
                for mate_key in tier_data[pkm_key]["Teammates"]:
                    session.execute_write(link_mates_pkms, pkm_key.lower(), mate_key.lower(), tier_data[pkm_key]["Teammates"][mate_key], tier_name)
    
    def add_tier_data_fast(self, tier_data, tier_name) :
        '''
        Add the tier data to the database
        param tier_data: tier data to be loaded
        param tier_name: name of the tier
        '''
        tier_data = tier_data["data"]
        with self.driver.session(database="pokedb") as session :
            with session.begin_transaction() as tx:
                for pkm_key in list(tier_data.keys()):
                    #Link to tier
                    #tx.run(link_to_tier, pkm_key.lower(), tier_name)
                    link_to_tier(tx, pkm_key.lower(), tier_name)
                    #tx.run("MATCH (p:Pokemon {name: $pkm_name}), (t:Tier {name: $tier_name}) CREATE (p)-[r:IN_TIER]->(t)", pkm_name=pkm_key.lower(), tier_name=tier_name)
                    #Add link to teammates
                    for mate_key in tier_data[pkm_key]["Teammates"]:
                        #tx.run(link_mates_pkms, pkm_key.lower(), mate_key.lower(), tier_data[pkm_key]["Teammates"][mate_key], tier_name)
                        link_mates_pkms(tx, pkm_key.lower(), mate_key.lower(), tier_data[pkm_key]["Teammates"][mate_key], tier_name)
                        #tx.run("MATCH (p1:Pokemon {name: $pkm1}),(p2:Pokemon {name: $pkm2}) CREATE (p1)-[r:LINK {value: $link_value, name: $tier_name}]->(p2)", pkm1=pkm_key.lower(), pkm2=mate_key.lower(), link_value=tier_data[pkm_key]["Teammates"][mate_key], tier_name=tier_name)

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
            tiers_response = session.run("MATCH (t:Tier) RETURN t.name ORDER BY t.name")
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

#Static functions for the database -----------------------------------
def create_tier(tx, name) :
    '''
    Creates a tier node
    param tx: transaction
    param name: name of the tier
    '''
    tx.run("CREATE (t:Tier {name: $name})", name=name)

def create_pokemon(tx, name, num, stats, heightm, weightkg):
    '''
    Creates a pokemon node
    param tx: transaction
    param name: name of the pokemon
    param num: pokedex number of the pokemon
    param stats: stats of the pokemon
    param heightm: height of the pokemon in meters
    param weightkg: weight of the pokemon in kilograms
    '''
    tx.run("CREATE (p:Pokemon {name: $name, num: $num, st_hp: $st_hp, st_atk: $st_atk, st_def: $st_def, st_spa: $st_spa, st_spd: $st_spd, st_spe: $st_spe, heightm: $heightm, weightkg: $weightkg})", name=name, num=num, st_hp=stats['hp'], st_atk=stats['atk'], st_def=stats['def'], st_spa=stats['spa'], st_spd=stats['spd'], st_spe=stats['spe'], heightm=heightm, weightkg=weightkg)

def link_to_tier(tx, pkm_name, tier_name):
    '''
    Links a pokemon to a tier
    param tx: transaction
    param pkm_name: name of the pokemon
    param tier_name: name of the tier
    '''
    #Create the link between the pokemon and the tier
    tx.run("MATCH (p:Pokemon {name: $pkm_name}), (t:Tier {name: $tier_name}) CREATE (p)-[r:IN_TIER]->(t)", pkm_name=pkm_name, tier_name=tier_name)
def link_mates_pkms(tx, pkm1, pkm2, link_value, tier_name):
    '''
    Links two pokemon nodes
    param tx: transaction
    param pkm1: name of the first pokemon
    param pkm2: name of the second pokemon
    param link_value: value of the link
    param tier_name: name of the tier
    '''
    #Link the two pokemon and assign value to the link and set name according to tier name
    tx.run("MATCH (p1:Pokemon {name: $pkm1}),(p2:Pokemon {name: $pkm2}) CREATE (p1)-[r:LINK {value: $link_value, name: $tier_name}]->(p2)", pkm1=pkm1, pkm2=pkm2, link_value=link_value, tier_name=tier_name)

def link_types_pokemon(tx, pkm_name, type_name):
    '''
    Links a pokemon to a type
    param tx: transaction
    param pkm_name: name of the pokemon
    param type_name: name of the type
    '''
    tx.run("MATCH (p:Pokemon {name: $pkm_name}), (t:Type {name: $type_name}) CREATE (p)-[:IS_OF_TYPE]->(t)", pkm_name=pkm_name, type_name=type_name)

def link_evolution(tx, pkm_name, evo_name):
    '''
    Links a pokemon to its evolution
    param tx: transaction
    param pkm_name: name of the pokemon
    param evo_name: name of the evolution
    '''
    tx.run("MATCH (p:Pokemon {name: $pkm_name}), (e:Pokemon {name: $evo_name}) CREATE (p)-[:EVOLVES_TO]->(e)", pkm_name=pkm_name, evo_name=evo_name)

def load_json(file_path: str) -> dict:
    """
    Loads a json file and returns it as a dict
    """
    #Load json utf-8


    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data

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
    db_handler.clear_mates_links()
    #Load every tiers .json files tracked 
    files_tracked = load_json(r"D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\settings.json")

    for tier in files_tracked["tiersTracked"]:
        if db_handler.check_if_node_exists("Tier", "name", tier) == False:
            #Create the tier node
            with db_handler.driver.session() as session:
                session.write_transaction(create_tier, tier)
        #Add data to db 
        file_name = files_tracked["tiersTracked"][tier]["fileNameShowdown"]
        tier_data = load_json_url("https://www.smogon.com/stats/2022-11/chaos/{}".format(file_name))
        db_handler.add_tier_data_fast(tier_data=tier_data, tier_name=tier)
        print("Done for {}".format(tier))
    print("Time taken : {}".format(time.time() - start_time))
    print("Done")



if __name__ == "__main__" :
    '''
    When the script running as main, the database is updated with the data from the tiers tracked
    '''
    update_db()


    




