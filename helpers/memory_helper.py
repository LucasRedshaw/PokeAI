def get_coords(GameBoyEnv):
    mapid = GameBoyEnv.pyboy.memory[0xD35E]
    xcoord = GameBoyEnv.pyboy.memory[0xD362]
    ycoord = GameBoyEnv.pyboy.memory[0xD361]
    coords = (mapid, xcoord, ycoord)

    return coords, mapid

def get_level_sum(GameBoyEnv):
    poke1lvl = GameBoyEnv.pyboy.memory[0xD18C]      
    poke2lvl = GameBoyEnv.pyboy.memory[0xD1B8]
    poke3lvl = GameBoyEnv.pyboy.memory[0xD1E4]
    poke4lvl = GameBoyEnv.pyboy.memory[0xD210]
    poke5lvl = GameBoyEnv.pyboy.memory[0xD23C]
    poke6lvl = GameBoyEnv.pyboy.memory[0xD268]
    pokelvlsum = poke1lvl + poke2lvl + poke3lvl + poke4lvl + poke5lvl + poke6lvl

    return pokelvlsum

def get_opponent_level(GameBoyEnv):
    
    opponentlvl1 = GameBoyEnv.pyboy.memory[0xD8C5]
    opponentlvl2 = GameBoyEnv.pyboy.memory[0xD8F1]
    opponentlvl3 = GameBoyEnv.pyboy.memory[0xD91D]
    opponentlvl4 = GameBoyEnv.pyboy.memory[0xD949]
    opponentlvl5 = GameBoyEnv.pyboy.memory[0xD975]
    opponentlvl6 = GameBoyEnv.pyboy.memory[0xD9A1]
    opponentlvlsum = opponentlvl1 + opponentlvl2 + opponentlvl3 + opponentlvl4 + opponentlvl5 + opponentlvl6

    return opponentlvlsum

def get_hp(GameBoyEnv):
    poke1maxhp1 = GameBoyEnv.pyboy.memory[0xD18D]
    poke1maxhp2 = GameBoyEnv.pyboy.memory[0xD18E]
    poke1currenthp1 = GameBoyEnv.pyboy.memory[0xD16C]
    poke1currenthp2 = GameBoyEnv.pyboy.memory[0xD16D]
    poke1maxhp = poke1maxhp1 + poke1maxhp2
    poke1currenthp = poke1currenthp1 + poke1currenthp2

    poke2maxhp1 = GameBoyEnv.pyboy.memory[0xD1B9]
    poke2maxhp2 = GameBoyEnv.pyboy.memory[0xD1BA]
    poke2currenthp1 = GameBoyEnv.pyboy.memory[0xD198]
    poke2currenthp2 = GameBoyEnv.pyboy.memory[0xD199]
    poke2maxhp = poke2maxhp1 + poke2maxhp2
    poke2currenthp = poke2currenthp1 + poke2currenthp2

    poke3maxhp1 = GameBoyEnv.pyboy.memory[0xD1E5]
    poke3maxhp2 = GameBoyEnv.pyboy.memory[0xD1E6]
    poke3currenthp1 = GameBoyEnv.pyboy.memory[0xD1C4]
    poke3currenthp2 = GameBoyEnv.pyboy.memory[0xD1C5]
    poke3maxhp = poke3maxhp1 + poke3maxhp2
    poke3currenthp = poke3currenthp1 + poke3currenthp2

    poke4maxhp1 = GameBoyEnv.pyboy.memory[0xD211]
    poke4maxhp2 = GameBoyEnv.pyboy.memory[0xD212]
    poke4currenthp1 = GameBoyEnv.pyboy.memory[0xD1F0]
    poke4currenthp2 = GameBoyEnv.pyboy.memory[0xD1F1]
    poke4maxhp = poke4maxhp1 + poke4maxhp2
    poke4currenthp = poke4currenthp1 + poke4currenthp2

    poke5maxhp1 = GameBoyEnv.pyboy.memory[0xD23D]
    poke5maxhp2 = GameBoyEnv.pyboy.memory[0xD23E]
    poke5currenthp1 = GameBoyEnv.pyboy.memory[0xD21C]
    poke5currenthp2 = GameBoyEnv.pyboy.memory[0xD21D]
    poke5maxhp = poke5maxhp1 + poke5maxhp2
    poke5currenthp = poke5currenthp1 + poke5currenthp2

    poke6maxhp1 = GameBoyEnv.pyboy.memory[0xD269]
    poke6maxhp2 = GameBoyEnv.pyboy.memory[0xD26A]
    poke6currenthp1 = GameBoyEnv.pyboy.memory[0xD248]
    poke6currenthp2 = GameBoyEnv.pyboy.memory[0xD249]
    poke6maxhp = poke6maxhp1 + poke6maxhp2
    poke6currenthp = poke6currenthp1 + poke6currenthp2

    summaxhp = poke1maxhp + poke2maxhp + poke3maxhp + poke4maxhp + poke5maxhp + poke6maxhp
    sumcurrenthp = poke1currenthp + poke2currenthp + poke3currenthp + poke4currenthp + poke5currenthp + poke6currenthp

    hptracker = sumcurrenthp / summaxhp

    return hptracker, sumcurrenthp, summaxhp 