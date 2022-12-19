class TeamMember :
    def __init__(self, name=""):
        self.name = name
        self.image_url = "assets/images/default.png"
    
    def get_data(self):
        return {
            "name" : self.name,
            "imageUrl" : self.image_url
        }
    