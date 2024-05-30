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

        exploration_reward = 1

        if mapid == 1:
            #print("Viridian City")
            exploration_reward += 0.2
        if mapid == 12:
            #print("Route 1")
            exploration_reward += 0.1
        if mapid == 51:
            #print("Viridian Forest")
            exploration_reward += 0.3
        if mapid == 50:
            #print("Viridian Forest")
            exploration_reward += 0.3
        if mapid == 47:
            #print("Viridian Forest")
            exploration_reward += 0.3
        if mapid == 13:
            #print("Route 2")
            exploration_reward += 0.3
        if mapid == 2:
            #print("Pewter City")
            exploration_reward += 0.4
        GameBoyEnv.seen_coords.add(coords)

        #coordreward = (0.02 * len(self.seen_coords))

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
        level_rewards = 50*(pokelvlsum - GameBoyEnv.pokelvlsumtrack)
        #levelupreward = 8
        #print("Caught or Levelled")
        GameBoyEnv.pokelvlsumtrack = pokelvlsum

    # levelupreward = (0.2 *(pokelvlsum - 6))
    return level_rewards

