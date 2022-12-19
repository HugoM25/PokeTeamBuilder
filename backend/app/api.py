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
        return response, 200

@app.route('/get_pkm_in_tier', methods=["POST"])
def get_pkm_in_tier():
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

        #Create a team builder
        team_builder = pokeTeamPy.TeamBuilder()

        #Complete team 
        team_builder.complete_team(json_data["format"], json_data["team"])

        #Get the team
        team = team_builder.get_team()

        response = jsonify(team)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 201




if __name__ == '__main__':
    db_handler = pokeTeamPy.DataBaseHandler()
    app.run(debug=True)