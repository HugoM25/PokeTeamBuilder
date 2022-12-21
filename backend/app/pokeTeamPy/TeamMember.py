class TeamMember :
    def __init__(self, name="", image_url="assets/images/default.png", locked=False ):
        self.name = name
        if name != "" :
            self.image_url = "https://play.pokemonshowdown.com/sprites/ani/" + name + ".gif"
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
    