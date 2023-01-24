from .utils import write_ev_spread
class TeamMember :
    def __init__(self, name="", image_url="assets/images/default.png", locked=False, settings=None):
        self.name = name
        if name != "" :
            """
            #Handle exceptions (names with '-' char)
            if settings is not None:
                if name in settings["spritesExceptions"].keys():
                    print("Exception found")
                    self.image_url = "https://play.pokemonshowdown.com/sprites/ani/" + settings["spritesExceptions"][name] + ".gif"
                    print(self.image_url)
                else : 
                    self.image_url = "https://play.pokemonshowdown.com/sprites/ani/" + name + ".gif"
            else :
                self.image_url = "https://play.pokemonshowdown.com/sprites/ani/" + name + ".gif"
            """
            #Till gen9 gifs are not available use this one
            if settings is not None:
                if name in settings["spritesExceptions"].keys():
                    self.image_url = "https://play.pokemonshowdown.com/sprites/dex/" + settings["spritesExceptions"][name] + ".png"                    
                elif "mega" in name :
                    self.image_url = "https://play.pokemonshowdown.com/sprites/dex/" + name.replace("mega", "") + ".png"  
                elif "megax" in name :
                    self.image_url = "https://play.pokemonshowdown.com/sprites/dex/" + name.replace("megax", "") + ".png"
                elif "megay" in name :
                    self.image_url = "https://play.pokemonshowdown.com/sprites/dex/" + name.replace("megay", "") + ".png"    
                else : 
                    self.image_url = "https://play.pokemonshowdown.com/sprites/dex/" + name + ".png"
            else :
                self.image_url = "https://play.pokemonshowdown.com/sprites/dex/" + name + ".png"
            
        else :
            self.image_url = image_url
        self.locked = locked
        self.moves = []
        self.item = ""
        self.ability = ""
        self.nature = "Hardy"
        self.spread=""

    def compose_set(self, db_handler, tier_name) :
        #Set the item 
        self.item = db_handler.get_thing_for_pkm(self.name, "Item","USES",tier_name, 1)[0]["i"]
        
        #Set the ability
        self.ability = db_handler.get_thing_for_pkm(self.name, "Ability","HAS",tier_name, 1)[0]["i"]
       
        #Set the moves
        moves_list = db_handler.get_thing_for_pkm(self.name, "Move","KNOWS",tier_name, 4)
        
        for i in range(0,4) :
            self.moves.append(Move(moves_list[i]["i"]["name"], moves_list[i]["i"]))
            
        #Set the spread
        spread_infos = db_handler.get_thing_for_pkm(self.name, "Spread","HAS_SPREAD",tier_name, 1)[0]["i"]
        self.ev_spread = write_ev_spread(spread_infos)
        self.nature = spread_infos["nature"]
    

    def get_data(self):
        return {
            "name" : self.name,
            "imageUrl" : self.image_url,
            "isLocked" : self.locked
        }

    def get_showdown_format(self):
        pkm_showdown_format = f"""
        {self.name} @ {self.item["name"]}  
        Ability: {self.ability["name"]}
        EVs: {self.ev_spread}  
        {self.nature.capitalize()} Nature
        - {self.moves[0].name}  
        - {self.moves[1].name}   
        - {self.moves[2].name}    
        - {self.moves[3].name} 
        """
        return pkm_showdown_format


    def __repr__(self) -> str:
        return self.name + str(self.locked)
    


class Move :
    def __init__(self, move_name="", dict_object=None): 
        if dict_object is not None:
            self.name = move_name
            self.category = dict_object["category"]
            self.accuracy = int(dict_object["accuracy"])
            self.base_power = int(dict_object["power"])
            self.pp = int(dict_object["pp"]) 
        else :
            self.name =move_name
            self.type = ""
            self.category = ""
            self.accuracy = 0
            self.base_power = 0
            self.pp = 0

class MoveDb :
    def __init__(self, move_name="", json_object=None): 
        if json_object is not None:
            self.name = move_name
            self.type = json_object["type"]
            self.category = json_object["category"]
            self.accuracy = int(json_object["accuracy"])
            self.base_power = int(json_object["basePower"])
            self.pp = int(json_object["pp"]) 
        else :
            self.name =move_name
            self.type = ""
            self.category = ""
            self.accuracy = 0
            self.base_power = 0
            self.pp = 0




    

