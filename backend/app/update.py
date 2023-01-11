from pokeTeamPy import *
import time 

def update_db():
    start_time = time.time()
    db_handler = DataBaseHandler()
    #Remove links mate data 
    db_handler.clear_current_tiers_links()

    #Load every tiers .json files tracked 
    files_tracked = load_json(r"D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\settings.json")

    for tier in files_tracked["tiersTracked"]:
        if db_handler.check_if_node_exists("Tier", "name", tier) == False:
            #Create the tier node
            with db_handler.driver.session() as session:
                session.write_transaction(dbu.create_tier, tier)
        #Add data to db 
        file_name = files_tracked["tiersTracked"][tier]["fileNameShowdown"]
        tier_data = load_json_url("https://www.smogon.com/stats/2022-12/chaos/{}".format(file_name))
        db_handler.add_tier_data_godspeed(tier_data=tier_data, tier_name=tier)
        print("Done for {}".format(tier))

    #Now that tiers are loaded in the db, we can look at some stats for the tiers : 
    

    print("Time taken : {}".format(time.time() - start_time))
    print("Done")

def test_db(): 
    tier_data = load_json(r"D:\ProjetsPersos\PokeTeamBuilder\backend\app\static\Json\gen8ou-0.json")
    spreads = { 
        "natures" : [],
        "hp_evs" : [], 
        "atk_evs" : [],
        "def_evs" : [],
        "spa_evs" : [],
        "spd_evs" : [],
        "spe_evs" : []
    }
    c = 0
    for pkm_key in tier_data['data'].keys() : 
        print("another poke : ", pkm_key)
        for spread in tier_data['data'][pkm_key]["Spreads"] :
            if tier_data['data'][pkm_key]["Spreads"][spread] >100: 
                c += 1
                print(spread)
    print(c)



#How to store the spreads into the database ?
#select 30 or less most used spreads for each pokemon
#Create node foreach spread
#Add link


if __name__ == "__main__" :
    update_db()