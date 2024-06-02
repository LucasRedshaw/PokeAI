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
    pokemon_centers = memory_helper.pokemon_centers
    heal_reward = 0
    if mapid in pokemon_centers and hpcurrent > GameBoyEnv.hpold:
        heal_reward = 0.075 * (hpmax - GameBoyEnv.hpold)
        GameBoyEnv.hpold = hpcurrent
        print("healed at", pokemon_centers[mapid])
    else:
        GameBoyEnv.hpold = hpcurrent
    return heal_reward



def calc_exploration_reward(GameBoyEnv):
    coords, mapid = memory_helper.get_coords(GameBoyEnv)
    GameBoyEnv.mapid = mapid
    exploration_reward = 0
    coordvalue = 0.01  # Default coordinate value

    if coords not in GameBoyEnv.seen_coords:
        if mapid not in GameBoyEnv.seen_maps:
            if mapid in memory_helper.locations:
                print(memory_helper.locations[mapid])
            if mapid in memory_helper.pokemon_centers:
                print(memory_helper.pokemon_centers[mapid])
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

