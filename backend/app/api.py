from flask import Flask, jsonify, request
from flask_cors import CORS
from pokeTeamPy import *

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def test():
    pokeList = [
        {"id": 1, "name": 'bulbasaur', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'},
        {"id": 2, "name": 'charmander', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png'},
        {"id": 3, "name": 'squirtle', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png'},
        {"id": 4, "name": 'lapras', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/131.png'},
        {"id": 5, "name": 'gengar', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png'},
        {"id": 6, "name": 'pikachu', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'}
    ] 
    response = jsonify(pokeList)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/set_pkm', methods=["POST"])
def set_pkm():
    if request.method == "POST" :
        #Get the data from the request
        json_data = request.get_json()
        #Create a pokemon response
        pokeInfos = {
            "name": json_data["name"].lower(),
            "imageUrl": "https://play.pokemonshowdown.com/sprites/dex/" + json_data["name"].lower() + ".png"
        }
        #Return the response
        response = jsonify(pokeInfos)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/pkm_list', methods=["GET"])
def pkm_list():
    response = None
    if request.method == "GET" :
        nameList = [
            'bulbasaur',
            'charmander',
            'squirtle',
            'lapras',
            'gengar',
            'pikachu',
            'dragonite',
            'mewtwo',
            'mew',
            'snorlax',
            'articuno',
            'zapdos',
            'moltres',
        ]
        response = jsonify(nameList)
        print(response)
        response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)