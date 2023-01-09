from flask import Flask, jsonify, request
from flask_cors import CORS
import pokeTeamPy


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def test():
    response = None
    if request.method == "GET":
        team_builder = pokeTeamPy.TeamBuilder()
        response = jsonify(team_builder.get_team())
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Set-Cookie','cross-site-cookie=bar; SameSite=None; Secure')

        return response, 200

@app.route('/get_pkm', methods=["POST"])
def get_pkm():
    '''
    Get the pokemon with the given name
    '''
    response = None
    if request.method == "POST":
        #Get the data from the request
        json_data = request.get_json()

        #Get the pokemon
        pkm = pokeTeamPy.TeamMember(str(json_data["name"]))

        pkm.image_url = "https://play.pokemonshowdown.com/sprites/ani/" + pkm.name + ".gif"
        #Create the response
        response = jsonify(pkm.get_data())
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Set-Cookie','cross-site-cookie=bar; SameSite=None; Secure')

        return response, 200

@app.route('/get_pkms_in_tier', methods=["POST"])
def get_pkms_in_tier():
    '''
    Get all pokemon in a given tier
    '''
    response = None
    if request.method == "POST":
        #Get the data from the request
        json_data = request.get_json()

        #Get the pokemon in the given tier
        pkm_names = db_handler.get_pokemons_in_tier(str(json_data["tier"]))

        #Create the response
        response = jsonify(pkm_names)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Set-Cookie','cross-site-cookie=bar; SameSite=None; Secure')

        return response, 200

@app.route('/get_tiers', methods=["GET"])
def get_tiers():
    '''
    Get the tiers available in the database
    '''
    response = None
    if request.method == "GET":
        #Get the tiers
        tiers = db_handler.get_tiers()

        #Create the response
        response = jsonify(tiers)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Set-Cookie','cross-site-cookie=bar; SameSite=None; Secure')

        return response, 200
        
    
@app.route('/complete_team', methods=["POST"])
def complete_team():
    '''
    Complete a team with pokemon from the given format
    '''
    response = None
    if request.method == "POST":
        #Get the data from the request
        json_data = request.get_json()

        curr_team = [member for member in json_data["team"]]
        #Create a team builder
        team_builder = pokeTeamPy.TeamBuilder(curr_team, tier=json_data["tier"], db_handler=db_handler)

        #Complete team 
        team_builder.complete_team(method="JSP")

        #Get the team
        team = team_builder.get_team()
        response = jsonify(team)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Set-Cookie','cross-site-cookie=bar; SameSite=None; Secure')

        return response, 200
    




if __name__ == '__main__':
    db_handler = pokeTeamPy.DataBaseHandler()
    app.run(debug=True)