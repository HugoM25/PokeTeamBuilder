import json
import re


def load_json(file_path: str) -> dict:
    """
    Loads a json file and returns it as a dict
    """
    #Load json utf-8
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_pokemon_names_in_format(format_name: str) -> list:
    """
    Returns a list of all pokemon names in a given format
    """
    data = load_json("backend/app/pokeTeamPy/static/Json/gen8ou-0.json")
    print(data)
    pkm_names = list(data['data'].keys())
    return pkm_names


def is_pkm_in_format(pkm_name: str, format_name: str) -> bool:
    """
    Returns True if the given pokemon is in the given format, False otherwise
    """
    return pkm_name in get_pokemon_names_in_format(format_name)


def remove_non_letters(string):
    return re.sub(r'[^a-zA-Z0-9]', '', string)


def clean_names(name) : 
    return remove_non_letters(name).lower()


def spread_to_dict(spread_string) :
    splitted_stats = spread_string.split(':')[1].split('/')
    spread = {
        "nature" : spread_string.split(':')[0].lower(),
        "ev_hp" : splitted_stats[0],
        "ev_atk" : splitted_stats[1],
        "ev_def" : splitted_stats[2],
        "ev_spa" : splitted_stats[3],
        "ev_spd" : splitted_stats[4],
        "ev_spe" : splitted_stats[5]
    }
    return spread

def dict_to_neo4j_style(spread_string) : 
    #Transform the 'key': in key:
    return spread_string.replace("{'", "{").replace("':", ":").replace(", '", ", ")

def write_ev_spread(evs_data):
    #In the format  Evs: 252 Atk / 252 Spe / 4 SpD
    return evs_data["ev_hp"] + " Hp / " + evs_data["ev_atk"] + " Atk / " + evs_data["ev_def"] + " Def / " + evs_data["ev_spa"] + " SpA / " + evs_data["ev_spd"] + " SpD / " + evs_data["ev_spe"] + " Spe"
