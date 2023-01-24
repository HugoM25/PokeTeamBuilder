from neo4j import GraphDatabase

#Static functions for the database -----------------------------------

def query_find_next_best_poke(tx, team) :
    '''
    Finds the next best pokemon to add to a team
    param tx: transaction
    param team: list of pokemon names
    '''
    tx.run("MATCH (p:Pokemon)-[r:LINK]->(m:Pokemon) WHERE p.name IN $team AND r.name = 'GEN8OU' AND NOT m.name IN $team WITH m, sum(r.value) as totalMateValue ORDER BY totalMateValue DESC LIMIT 10 RETURN m.name as nextBestMates , totalMateValue", team=team)


def query_create_move(tx, move):
    '''
    Creates a move node
    param tx: transaction
    param move: object of type Move
    '''
    tx.run("CREATE (m:Move {name: $name, power: $power, accuracy: $accuracy, pp: $pp, category: $category})", name=move.name, power=move.base_power, accuracy=move.accuracy, pp=move.pp, category=move.category)

def query_link_move_to_type(tx, move_name, type_name):
    '''
    Links a move to a type
    param tx: transaction
    param move_name: name of the move
    param type_name: name of the type
    '''
    tx.run("MATCH (m:Move {name: $move_name}), (t:Type {name: $type_name}) CREATE (m)-[:IS]->(t)", move_name=move_name, type_name=type_name)



def query_create_item(tx, item_node_name, item_well_written_name,item_sprite_num, item_num) :
    '''
    Creates an item node
    param tx: transaction
    param item_node_name: name of the item
    param item_well_written_name: well written name of the item
    param item_sprite_num: sprite number of the item
    param item_num: pokedex number of the item
    '''
    tx.run("CREATE (i:Item {name: $name, wellWrittenName: $wellWrittenName, sprite_num: $sprite_num, num: $num})", name=item_node_name, wellWrittenName=item_well_written_name ,sprite_num=item_sprite_num, num=item_num)

def query_link_pkm_to_item(tx, item_name, pokemon_name, value, tier) :
    '''
    Links a pokemon to an item
    param tx: transaction
    param item_name: name of the item
    param pokemon_name: name of the pokemon
    param tier: tier of the pokemon
    param value: value of the item
    '''
    tx.run("MATCH (p:Pokemon {name: $pkm_name}), (i:Item {name: $item_name}) CREATE (p)-[:USES {tier: $tier, value: $value}]->(i)", pkm_name=pokemon_name, item_name=item_name, tier=tier, value=value)

def query_link_pkm_to_ability(tx, ability_name, pokemon_name, value, tier):
    '''
    Links a pokemon to an ability
    param tx: transaction
    param ability_name: name of the ability
    param pokemon_name: name of the pokemon
    param value: value of the ability
    param tier: tier of the pokemon
    '''
    tx.run("MATCH (p:Pokemon {name: $pkm_name}), (a:Ability {name: $ability_name}) CREATE (p)-[:HAS {tier: $tier, value: $value}]->(a)", pkm_name=pokemon_name, ability_name=ability_name, value=value, tier=tier)

def query_create_ability(tx, ability_node_name, ability_well_written_name, ability_num, ability_rating) :
    '''
    Creates an ability node
    param tx: transaction
    param ability_node_name: name of the ability
    param ability_well_written_name: well written name of the ability
    param ability_num: pokedex number of the ability
    '''
    tx.run("CREATE (a:Ability {name: $name, wellWrittenName: $wellWrittenName, num: $num, rating: $rating})", name=ability_node_name, wellWrittenName=ability_well_written_name, num=ability_num, rating=ability_rating)

def query_create_tier(tx, name) :
    '''
    Creates a tier node
    param tx: transaction
    param name: name of the tier
    '''
    tx.run("CREATE (t:Tier {name: $name})", name=name)

def query_create_pokemon(tx, name, num, stats, heightm, weightkg):
    '''
    Creates a pokemon node
    param tx: transaction
    param name: name of the pokemon
    param num: pokedex number of the pokemon
    param stats: stats of the pokemon
    param heightm: height of the pokemon in meters
    param weightkg: weight of the pokemon in kilograms
    '''
    tx.run("CREATE (p:Pokemon {name: $name, num: $num, st_hp: $st_hp, st_atk: $st_atk, st_def: $st_def, st_spa: $st_spa, st_spd: $st_spd, st_spe: $st_spe, heightm: $heightm, weightkg: $weightkg})", name=name, num=num, st_hp=stats['hp'], st_atk=stats['atk'], st_def=stats['def'], st_spa=stats['spa'], st_spd=stats['spd'], st_spe=stats['spe'], heightm=heightm, weightkg=weightkg)

def query_link_to_tier(tx, pkm_name, tier_name, count):
    '''
    Links a pokemon to a tier
    param tx: transaction
    param pkm_name: name of the pokemon
    param tier_name: name of the tier
    param count: number of times the pokemon was used in the tier
    '''
    #Create the link between the pokemon and the tier
    query = f"""MATCH (p:Pokemon {{name: "{pkm_name}"}}), (t:Tier {{name: "{tier_name}"}}) CREATE (p)-[r:IN_TIER {{value: {count} }}]->(t)"""
    tx.run(query)

def query_link_mates_pkms(tx, pkm1, pkm2, link_value, tier_name):
    '''
    Links two pokemon nodes
    param tx: transaction
    param pkm1: name of the first pokemon
    param pkm2: name of the second pokemon
    param link_value: value of the link
    param tier_name: name of the tier
    '''
    #Link the two pokemon and assign value to the link and set name according to tier name
    tx.run("MATCH (p1:Pokemon {name: $pkm1}),(p2:Pokemon {name: $pkm2}) CREATE (p1)-[r:LINK {value: $link_value, name: $tier_name}]->(p2)", pkm1=pkm1, pkm2=pkm2, link_value=link_value, tier_name=tier_name)

def query_link_types_pokemon(tx, pkm_name, type_name):
    '''
    Links a pokemon to a type
    param tx: transaction
    param pkm_name: name of the pokemon
    param type_name: name of the type
    '''
    tx.run("MATCH (p:Pokemon {name: $pkm_name}), (t:Type {name: $type_name}) CREATE (p)-[:IS_OF_TYPE]->(t)", pkm_name=pkm_name, type_name=type_name)

def query_link_evolution(tx, pkm_name, evo_name):
    '''
    Links a pokemon to its evolution
    param tx: transaction
    param pkm_name: name of the pokemon
    param evo_name: name of the evolution
    '''
    tx.run("MATCH (p:Pokemon {name: $pkm_name}), (e:Pokemon {name: $evo_name}) CREATE (p)-[:EVOLVES_TO]->(e)", pkm_name=pkm_name, evo_name=evo_name)


def query_find_pokemon_of_type(tx, type_name):
    '''
    Finds all the pokemon of a given type
    param tx: transaction
    param type_name: name of the type
    '''
    #Execute the query
    result = tx.run("MATCH (p:Pokemon)-[:IS_OF_TYPE]->(t:Type {name: $type_name}) RETURN p.name", type_name=type_name)
    #Return the result
    return result

def query_find_pokemon_of_tier_and_type(tx, tier_name, type_name):
    '''
    Finds all the pokemon of a given tier and type
    param tx: transaction
    param tier_name: name of the tier
    param type_name: name of the type
    '''
    #Finds all the pokemon of which belongs to the given tier and are of the given type
    result = tx.run("MATCH (p:Pokemon)-[:IN_TIER]->(t:Tier {name: $tier_name})-[:IS_OF_TYPE]->(t2:Type {name: $type_name}) RETURN p.name", tier_name=tier_name, type_name=type_name)
    return result

#-------------------------------------------------------------------------------
#The following queries are used to create the links using the tier monthly stats 
#They could be united in a single query but it would be less readable
#The query function would be something like:

def query_set_value_link_nodes(tx, link_type, node1_type, node2_type, node1_name, node2_name,property_name, value):
    '''
    Links two nodes
    @param tx: transaction
    @param node1_type: type of the first node
    @param node2_type: type of the second node
    @param node1_name: name of the first node
    @param node2_name: name of the second node
    @param property_name: name of the property
    @param value: value of the property
    '''
    tx.run(f"MATCH (n1:{node1_type})-[r:{link_type}]-(n2:{node2_type}) WHERE n1.name = '{node1_name}' AND n2.name = '{node2_name}' SET r.{property_name} = {value}")

def query_create_value_link_nodes(tx, link_type, node1_type, node2_type, node1_name, node2_name,property_name, value):
    '''
    Links two nodes
    @param tx: transaction
    @param node1_type: type of the first node
    @param node2_type: type of the second node
    @param node1_name: name of the first node
    @param node2_name: name of the second node
    @param property_name: name of the property
    @param value: value of the property
    '''
    tx.run(f"MATCH (n1:{node1_type}), (n2:{node2_type}) WHERE n1.name = '{node1_name}' AND n2.name = '{node2_name}' CREATE (n1)-[r:{link_type} {{{property_name}:{value}}}]->(n2)")

#----------------------------------------------
#Queries to link pokemon to moves

def query_set_value_link_moves(tx, pokemon_name, move_name, property_name, value):
    '''
    Links a pokemon to a move
    @param tx: transaction
    @param pokemon_name: name of the pokemon
    @param move_name: name of the move
    @param property_name: name of the tier 
    @param value: value of the property
    '''
    tx.run(f"MATCH (p1:Pokemon), (m:Move) WHERE p1.name = '{pokemon_name}' AND m.name = '{move_name}' SET r.{property_name} = {value}")

def query_create_value_link_moves(tx, pokemon_name, move_name, property_name, value):
    '''
    Links a pokemon to a move
    @param tx: transaction
    @param pokemon_name: name of the pokemon
    @param move_name: name of the move
    @param property_name: name of the tier 
    @param value: value of the property
    '''
    tx.run(f"MATCH (p1:Pokemon), (m:Move) WHERE p1.name = '{pokemon_name}' AND m.name = '{move_name}' CREATE (p1)-[r:LINK {{{property_name}:{value}}}]->(p2)")

#----------------------------------------------
#Queries to link pokemon mates 

def query_set_value_link_mates(tx, pkm1_name, pkm2_name, property_name, value):
    '''
    Links two pokemon nodes
    @param tx: transaction
    @param pkm1_name: name of the first pokemon
    @param pkm2_name: name of the second pokemon
    @param property_name: name of the property
    @param value: value of the property
    '''
    tx.run(f"MATCH (p1:Pokemon)-[r:LINK]-(p2:Pokemon) WHERE p1.name = '{pkm1_name}' AND p2.name = '{pkm2_name}' SET r.{property_name} = {value}") 

def query_create_link_mates(tx, pkm1_name, pkm2_name, property_name, value):
    '''
    Links two pokemon nodes
    @param tx: transaction
    @param pkm1_name: name of the first pokemon
    @param pkm2_name: name of the second pokemon
    @param property_name: name of the property
    @param value: value of the property
    '''
    tx.run(f"MATCH (p1:Pokemon), (p2:Pokemon) WHERE p1.name = '{pkm1_name}' AND p2.name = '{pkm2_name}' CREATE (p1)-[r:LINK {{{property_name}:{value}}}]->(p2)")



#Queries to link multiple pokemon mates to one

def query_set_list_node(tx, main_node_name, list_nodes_names, list_link_values, link_type, nodes_type, main_node_type, tier="GEN") :
    """
    Links multiple nodes to one
    @param tx: transaction
    @param main_node_name: name of the main node
    @param list_nodes_names: list of the names of the nodes to link
    @param list_link_values: list of the values of the links
    @param link_type: type of the link
    @param nodes_type: type of the nodes to link
    @param main_node_type: type of the main node
    """
    query = f"""WITH {list_link_values} as values, {list_nodes_names} AS names
               UNWIND names AS name
               MATCH (p:{nodes_type} {{name: name}})
               WITH p, name, reduce(acc = [], i IN range(0, size(values) - 1) | 
               acc + CASE WHEN names[i] = name THEN [values[i]] ELSE [] END) AS link_value
               MATCH (m:{main_node_type} {{name: "{main_node_name}"}})
               MERGE (p)-[r:{link_type}]->(m)
               SET r.{tier} = link_value[0]"""
    tx.run(query)

def query_set_list_spreads(tx, spreads_dict_item, spreads_dict_values, pokemon_name, tier, link_name="HAS_SPREAD") :
    #Use a query that will create a node from a map using the keys as properties
    query = f"""MATCH (m:Pokemon)
                WHERE m.name="{pokemon_name}"
                WITH m, [{str(spreads_dict_item)[2:-2].replace('}"', '}').replace('"{', '{')}] as items, {spreads_dict_values} as values
                UNWIND items as item
                MERGE (s:Spread {{nature:item["nature"], ev_hp:item["ev_hp"], ev_atk:item["ev_atk"], ev_def:item["ev_def"], 
                ev_spa:item["ev_spa"], ev_spd:item["ev_spd"], ev_spe:item["ev_spe"]}})
                WITH s, m, item, reduce(acc = [], i IN range(0, size(values) - 1) | 
                acc + CASE WHEN items[i] = item THEN [values[i]] ELSE [] END) AS link_value
                MERGE (s)-[r:{link_name}]->(m)
                SET r.{tier} = link_value[0]
            """
    tx.run(query)


def query_get_stats_on_tier(tx, tier): 
    """
    Get the stats of a tier
    @param tx: transaction
    @param tier: name of the tier
    """
    query = f"""match (t:Tier)-[r:IN_TIER]-(p:Pokemon) where t.name="{tier}" return sum(p.st_hp), sum(p.st_atk), sum(p.st_def), sum(p.st_spa), sum(p.st_spd), sum(p.st_spe), count(p), count(r.value)"""
    results =  tx.run(query)

def query_get_types_usage(tx,tier):
    """
    Get the types usage of a tier
    @param tx: transaction
    @param tier: name of the tier
    """
    query = f"""match (ty:Type)-[]-(p:Pokemon), (p)-[r:IN_TIER]-(ti:Tier) where ti.name="{tier}" return ty.name, sum(r.value) as nb_pkm order by nb_pkm desc"""
    results =  tx.run(query)
    return results

def query_get_average_stats(tx, tier):
    """
    Get the average stats of a tier
    @param tx: transaction
    @param tier: name of the tier
    """
    query = f"""match (p:Pokemon)-[r:IN_TIER]-(ti:Tier) where ti.name="{tier}" return sum(p.st_hp*r.value)/sum(r.value) as av_hp, sum(p.st_atk*r.value)/sum(r.value) as av_atk,  sum(p.st_def*r.value)/sum(r.value) as av_def,
            sum(p.st_spa*r.value)/sum(r.value) as av_spa, sum(p.st_spd*r.value)/sum(r.value) as av_spd, sum(p.st_spe*r.value)/sum(r.value) as av_spe, sum(r.value) as nb_pkm
            """
    results = tx.run(query)
    return results
