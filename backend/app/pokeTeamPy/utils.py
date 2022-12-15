
def load_json(file_path: str) -> dict:
    """
    Loads a json file and returns it as a dict
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    return data


def get_pokemon_names_in_format(format_name: str) -> list:
    """
    Returns a list of all pokemon names in a given format
    """
    data = load_json("backend/app/pokeTeamPy/static/Json/gen8ou-0.json")
    print(data)
    pkm_names = []
    return pkm_names

def is_pkm_in_format(pkm_name: str, format_name: str) -> bool:
    """
    Returns True if the given pokemon is in the given format, False otherwise
    """
    return pkm_name in get_pokemon_names_in_format(format_name)

