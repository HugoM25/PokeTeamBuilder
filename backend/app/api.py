from flask import Flask, jsonify, request
from flask_cors import CORS
import pokeTeamPy

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def test():
    pokeList = [
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
        pokeTeamPy
        response = jsonify(nameList)
        print(response)
        response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)