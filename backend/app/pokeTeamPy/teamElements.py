class TeamMember :
    def __init__(self, name="", image_url="assets/images/default.png", locked=False, settings=None):
        self.name = name
        if name != "" :
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
            
            #Till gen9 gifs are not available use this one
            #self.image_url = "https://play.pokemonshowdown.com/sprites/dex/" + name + ".png"
        else :
            self.image_url = image_url
        self.locked = locked
    
    def get_data(self):
        return {
            "name" : self.name,
            "imageUrl" : self.image_url,
            "isLocked" : self.locked
        }

    def __repr__(self) -> str:
        return self.name + str(self.locked)
    

class Move :
    def __init__(self, move_name="", json_object=None): 
        if json_object is not None:
            self.name = move_name
            self.type = json_object["type"]
            self.category = json_object["category"]
            self.accuracy = int(json_object["accuracy"])
            self.base_power = int(json_object["basePower"])
            self.pp = int(json_object["pp"]) 
        else :
            self.name =""
            self.type = ""
            self.category = ""
            self.accuracy = 0
            self.base_power = 0
            self.pp = 0




    

