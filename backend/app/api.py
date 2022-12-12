from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def test():

    pokeList = [
        {"id": 1, "name": 'Bulbasaur', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'},
        {"id": 2, "name": 'Charmander', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png'},
        {"id": 3, "name": 'Squirtle', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png'},
        {"id": 4, "name": 'Lapras', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/131.png'},
        {"id": 5, "name": 'Gengar', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png'},
        {"id": 6, "name": 'Pikachu', "imageUrl": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'}
    ] 
    response = jsonify(pokeList)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)