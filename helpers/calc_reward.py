from helpers import memory_helper
pokelvlsum = 0
badges = 0

def calc_reward(GameBoyEnv):
    exploration_reward = calc_exploration_reward(GameBoyEnv)
    level_reward = calc_level_reward(GameBoyEnv)
    heal_reward = calc_heal_reward(GameBoyEnv)
    faint_reward = calc_faint_reward(GameBoyEnv)
    battle_reward = calc_battle_reward(GameBoyEnv)
    badge_reward = calc_badge_reward(GameBoyEnv)
    reward = exploration_reward + level_reward + heal_reward + faint_reward + battle_reward + badge_reward
    return reward, exploration_reward, level_reward

def calc_badge_reward(GameBoyEnv):
    badges = memory_helper.get_badges(GameBoyEnv)
    badge_reward = 0
    if badges > GameBoyEnv.badges:
        badge_reward = 5
        GameBoyEnv.badges = badges
    return badge_reward

def calc_battle_reward(GameBoyEnv):
    battle_reward = 0
    opponentlvls = memory_helper.get_opponent_level(GameBoyEnv)
    if opponentlvls > 5 and opponentlvls != GameBoyEnv.opplvlold:
        battle_reward = 0.1*(opponentlvls)
        GameBoyEnv.opplvlold = opponentlvls
    return battle_reward

def calc_faint_reward(GameBoyEnv):
    hptracker = memory_helper.get_hp(GameBoyEnv)
    faint_reward = 0
    if hptracker == 0:
        if GameBoyEnv.wait1 == 0:
            print("Fainted")
            faint_reward = -0.1
            GameBoyEnv.wait1 = 1
    else:
        GameBoyEnv.wait1 = 0
    return faint_reward
    
def calc_heal_reward(GameBoyEnv):
    coords, mapid = memory_helper.get_coords(GameBoyEnv)
    hptrack, hpcurrent, hpmax = memory_helper.get_hp(GameBoyEnv)
    pokemon_centers = {
        41: "Pokémon Center (Viridian City)",
        58: "Pokémon Center (Pewter City)",
        64: "Pokémon Center (Cerulean City)",
        68: "Pokémon Center (Route 4)",
        81: "Pokémon Center (Rock Tunnel)",
        89: "Pokémon Center (Vermilion City)",
        133: "Pokémon Center (Celadon City)",
        141: "Pokémon Center (Lavender Town)",
        154: "Pokémon Center (Fuchsia City)",
        171: "Pokémon Center (Cinnabar Island)",
        174: "Pokémon Center (Indigo Plateau)",
        182: "Pokémon Center (Saffron City)"
    }
    heal_reward = 0
    if mapid in pokemon_centers and hpcurrent > GameBoyEnv.hpold:
        heal_reward = 0.05 * (hpmax - GameBoyEnv.hpold)
        GameBoyEnv.hpold = hpcurrent
        print("healed at", pokemon_centers[mapid])
    else:
        GameBoyEnv.hpold = hpcurrent
    return heal_reward

def calc_exploration_reward(GameBoyEnv):
    coords, mapid = memory_helper.get_coords(GameBoyEnv)
    exploration_reward = 0
    if coords not in GameBoyEnv.seen_coords:
        coordvalue = 0.01
        if mapid not in GameBoyEnv.seen_maps:

            if mapid == 1:
                print("Viridian City")
            if mapid == 12:
                print("Route 1")
            if mapid == 51:
                print("Viridian Forest")
            if mapid == 13:
                print("Route 2")
            if mapid == 2:
                print("Pewter City")
            if mapid == 41:
                print("Pokémon Center (Viridian City)")
                coordvalue = 2       
            if mapid == 58:
                print("Pokémon Center (Pewter City)")
                coordvalue = 2   
            if mapid == 64:
                print("Pokémon Center (Cerulean City)")
                coordvalue = 2   
            if mapid ==  68:
                print("Pokémon Center (Route 4)")
                coordvalue = 2   
            if mapid == 81:
                print("Pokémon Center (Rock Tunnel)")
                coordvalue = 2   
            if mapid == 89:
                print("Pokémon Center (Vermilion City)")
                coordvalue = 2   
            if mapid == 133:
                print("Pokémon Center (Celadon City)")
                coordvalue = 2   
            if mapid == 141:
                print("Pokémon Center (Lavender Town)")
                coordvalue = 2   
            if mapid == 154:
                print("Pokémon Center (Fuchsia City)")
                coordvalue = 2   
            if mapid == 171:
                print("Pokémon Center (Cinnabar Island)")
                coordvalue = 2   
            if mapid == 174:
                print("Pokémon Center (Indigo Plateau)")
                coordvalue = 2   
            if mapid == 182:
                print("Pokémon Center (Saffron City)")
                coordvalue = 2     

            GameBoyEnv.seen_maps.add(mapid)
        exploration_reward = coordvalue 
        GameBoyEnv.seen_coords.add(coords)
    return exploration_reward

def calc_level_reward(GameBoyEnv):
    pokelvlsum = memory_helper.get_level_sum(GameBoyEnv)
    level_rewards = 0
    if pokelvlsum > GameBoyEnv.pokelvlsumtrack:
        level_rewards = 0.25*(pokelvlsum - GameBoyEnv.pokelvlsumtrack)
        GameBoyEnv.pokelvlsumtrack = pokelvlsum
    return level_rewards

