from helpers import memory_helper
pokelvlsum = 0


def calc_reward(GameBoyEnv):

    exploration_reward = calc_exploration_reward(GameBoyEnv)
    level_reward = calc_level_reward(GameBoyEnv)
    heal_reward = calc_heal_reward(GameBoyEnv)
    faint_reward = calc_faint_reward(GameBoyEnv)
    battle_reward = calc_battle_reward(GameBoyEnv)

    reward = exploration_reward + level_reward + heal_reward + faint_reward + battle_reward

    return reward, exploration_reward, level_reward

def calc_battle_reward(GameBoyEnv):

    battle_reward = 0
    opponentlvls = memory_helper.get_opponent_level(GameBoyEnv)
    if opponentlvls > 5 and opponentlvls != GameBoyEnv.opplvlold:
        battle_reward = 0.1*(opponentlvls)
        GameBoyEnv.opplvlold = opponentlvls
        print(battle_reward)
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

    if mapid == 41 and hpcurrent > GameBoyEnv.hpold:

        heal_reward = 0.05*(hpmax - GameBoyEnv.hpold)

        GameBoyEnv.hpold = hpcurrent

        print("healed")

        return heal_reward
    else:

        heal_reward = 0
        GameBoyEnv.hpold = hpcurrent

        return heal_reward


def calc_exploration_reward(GameBoyEnv):

    coords, mapid = memory_helper.get_coords(GameBoyEnv)
    
    exploration_reward = 0

    if coords not in GameBoyEnv.seen_coords:

        coordvalue = 0.005
        #explorationvalue = (0.01 * len(GameBoyEnv.seen_coords))
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
                print("VC Pokecenter City")
                coordvalue = 2
                
            GameBoyEnv.seen_maps.add(mapid)
        exploration_reward = coordvalue 
        GameBoyEnv.seen_coords.add(coords)

    return exploration_reward

def calc_level_reward(GameBoyEnv):

    pokelvlsum = memory_helper.get_level_sum(GameBoyEnv)
    level_rewards = 0

    if pokelvlsum > GameBoyEnv.pokelvlsumtrack:
        level_rewards = 0.5*(pokelvlsum - GameBoyEnv.pokelvlsumtrack)
        GameBoyEnv.pokelvlsumtrack = pokelvlsum
        #print("Caught or Levelled")


    # levelupreward = (0.2 *(pokelvlsum - 6))
    return level_rewards

