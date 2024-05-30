from helpers import memory_helper

def calc_reward(GameBoyEnv):

    exploration_reward = calc_exploration_reward(GameBoyEnv)
    level_reward = calc_level_reward(GameBoyEnv)

    reward = exploration_reward + level_reward

    return reward, exploration_reward, level_reward

def calc_exploration_reward(GameBoyEnv):

    coords, mapid = memory_helper.get_coords(GameBoyEnv)
    
    exploration_reward = 0

    if coords not in GameBoyEnv.seen_coords:

        coordvalue = 1
        explorationvalue = (0.01 * len(GameBoyEnv.seen_coords))

        exploration_reward = coordvalue + explorationvalue

        GameBoyEnv.seen_coords.add(coords)

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
        GameBoyEnv.seen_maps.add(mapid)

    return exploration_reward

def calc_level_reward(GameBoyEnv):

    pokelvlsum = memory_helper.get_level_sum(GameBoyEnv)
    level_rewards = 0

    if pokelvlsum > GameBoyEnv.pokelvlsumtrack:
        level_rewards = pokelvlsum
        #levelupreward = 8
        #print("Caught or Levelled")
        GameBoyEnv.pokelvlsumtrack = pokelvlsum

    # levelupreward = (0.2 *(pokelvlsum - 6))
    return level_rewards

