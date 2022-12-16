from neo4j import GraphDatabase 
import json 

class DataBaseHandler:
    def __init__(self):
        self.uri = "neo4j://localhost:7687"
        #development password, will be changed at release
        self.driver = GraphDatabase.driver(self.uri, auth=("neo4j", "j4oen"))
    
    def load_pkm_data(self,json_data):
        """
        Load pokemon data into the database
        param json_data: json data to be loaded
        """
        with self.driver.session(database="pokedb") as session:
            for pkm_key in list(json_data.keys()):
                #Create the pokemon
                session.execute_write(create_pokemon, pkm_key)
                #Add the links to mates
                for mate_key in json_data[pkm_key]["Teammates"]:
                    session.execute_write(link_pokemons, pkm_key, mate_key, json_data[pkm_key]["Teammates"][mate_key])
                print("added", pkm_key)
        self.driver.close()

    def clear_db(self):
        """
        Clear the database
        """
        with self.driver.session(database="pokedb") as session:
            session.run("MATCH (n) DETACH DELETE n")
        self.driver.close()
    
        

def create_pokemon(tx, name):
    '''
    Creates a pokemon node
    param tx: transaction
    param name: name of the pokemon
    '''
    tx.run("CREATE (p:Pokemon {name: $name})", name=name)

def link_pokemons(tx, pkm1, pkm2, link_value):
    '''
    Links two pokemon nodes
    param tx: transaction
    param pkm1: name of the first pokemon
    param pkm2: name of the second pokemon
    param link_value: value of the link
    '''
    tx.run("MATCH (p1:Pokemon {name: $pkm1}),(p2:Pokemon {name: $pkm2}) CREATE (p1)-[r:LINK {value: $link_value}]->(p2)", pkm1=pkm1, pkm2=pkm2, link_value=link_value)



def load_json(file_path: str) -> dict:
    """
    Loads a json file and returns it as a dict
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data['data']

def get_pokemon_names_in_format(format_name: str) -> list:
    """
    Returns a list of all pokemon names in a given format
    """
    data = load_json("D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\gen8ou-0.json")
    print(data)
    pkm_names = list(data['data'].keys())
    return pkm_names


if __name__ == "__main__" :
    '''
    When running this file, it will create a database with the pokemon names using the json files"
    '''
    db_handler = DataBaseHandler()
    json_data = load_json(r"D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\gen8ou-0.json")
    db_handler.load_pkm_data(json_data)
    
    print("Done")

    #find linked pokemon with highest value to charizard
    with db_handler.driver.session(database="pokedb") as session:
        result = session.run("MATCH (p1:Pokemon {name: 'Charizard'})-[r:LINK]->(p2:Pokemon) RETURN p2.name, r.value ORDER BY r.value DESC LIMIT 5")
        for record in result:
            print(record)