# ######################################################################################
#                                        Ram_map
# ######################################################################################

# Data Crystal - https://datacrystal.romhacking.net/wiki/Pok%C3%A9mon_Red/Blue:RAM_map
# No Comments - https://github.com/pret/pokered/blob/91dc3c9f9c8fd529bb6e8307b58b96efa0bec67e/constants/event_constants.asm
# Comments - https://github.com/luckytyphlosion/pokered/blob/master/constants/event_constants.asm
from collections import deque
import numpy as np

CUT_GRASS_SEQ = deque([(0x52, 255, 1, 0, 1, 1), (0x52, 255, 1, 0, 1, 1), (0x52, 1, 1, 0, 1, 1)])
CUT_FAIL_SEQ = deque([(-1, 255, 0, 0, 4, 1), (-1, 255, 0, 0, 1, 1), (-1, 255, 0, 0, 1, 1)])
CUT_SEQ = [((0x3D, 1, 1, 0, 4, 1), (0x3D, 1, 1, 0, 1, 1)), ((0x50, 1, 1, 0, 4, 1), (0x50, 1, 1, 0, 1, 1)),]
HP_ADDR = [0xD16C, 0xD198, 0xD1C4, 0xD1F0, 0xD21C, 0xD248]
MAX_HP_ADDR = [0xD18D, 0xD1B9, 0xD1E5, 0xD211, 0xD23D, 0xD269]
PARTY_SIZE_ADDR = 0xD163
PARTY_ADDR = [0xD164, 0xD165, 0xD166, 0xD167, 0xD168, 0xD169]
PARTY_LEVEL_ADDR = [0xD18C, 0xD1B8, 0xD1E4, 0xD210, 0xD23C, 0xD268]
X_POS_ADDR = 0xD362
Y_POS_ADDR = 0xD361
MAP_N_ADDR = 0xD35E
BADGE_1_ADDR = 0xD356
WCUTTILE = 0xCD4D # 61 if Cut used; 0 default. resets to default on map_n change or battle.


GYM_LEADER = 5
GYM_TRAINER = 2
GYM_TASK = 2
RIVAL = 3

# EVENT #####################################################################################################

def gym1(pyboy):
   #gym 1 Pewter	
    one = GYM_LEADER * int(read_bit(pyboy, 0xD755, 7))
    g1_1 = GYM_TRAINER * int(read_bit(pyboy, 0xD755, 2)) #	"0xD755-2": "Beat Pewter Gym Trainer 0",
    return sum([one, g1_1, ])

def gym2(pyboy):
   #gym 2 Cerulean	
    two = GYM_LEADER * int(read_bit(pyboy, 0xD75E, 7))
    g2_1 = GYM_TRAINER * int(read_bit(pyboy, 0xD75E, 2)) #	"0xD75E-2": "Beat Cerulean Gym Trainer 0",
    g2_2 = GYM_TRAINER * int(read_bit(pyboy, 0xD75E, 3)) #	"0xD75E-3": "Beat Cerulean Gym Trainer 1",
    return sum([two, g2_1, g2_2, ])

def gym3(pyboy):
   #gym 3 Vermilion	
    lock_one = GYM_TASK * int(read_bit(pyboy, 0xD773, 1)) # "0xD773-1": "1S Lock Opened",
    lock_two = GYM_TASK * int(read_bit(pyboy, 0xD773, 0))# "0xD773-0": "2Nd Lock Opened",
    three = GYM_LEADER * int(read_bit(pyboy, 0xD773, 7))
    g3_1 = GYM_TRAINER * int(read_bit(pyboy, 0xD773, 2)) #	"0xD773-2": "Beat Vermilion Gym Trainer 0",
    g3_2 = GYM_TRAINER * int(read_bit(pyboy, 0xD773, 3)) #	"0xD773-3": "Beat Vermilion Gym Trainer 1",
    g3_3 = GYM_TRAINER * int(read_bit(pyboy, 0xD773, 4)) #	"0xD773-4": "Beat Vermilion Gym Trainer 2",
    return sum([three, g3_1, g3_2, g3_3, lock_one, lock_two])

def gym4(pyboy):
   #gym 4 Celadon	
    four = GYM_LEADER * int(read_bit(pyboy, 0xD792, 1))
    g4_1 = GYM_TRAINER * int(read_bit(pyboy, 0xD77C, 2)) #	"0xD77C-2": "Beat Celadon Gym Trainer 0",
    g4_2 = GYM_TRAINER * int(read_bit(pyboy, 0xD77C, 3)) #	"0xD77C-3": "Beat Celadon Gym Trainer 1",
    g4_3 = GYM_TRAINER * int(read_bit(pyboy, 0xD77C, 4)) #	"0xD77C-4": "Beat Celadon Gym Trainer 2",
    g4_4 = GYM_TRAINER * int(read_bit(pyboy, 0xD77C, 5)) #	"0xD77C-5": "Beat Celadon Gym Trainer 3",
    g4_5 = GYM_TRAINER * int(read_bit(pyboy, 0xD77C, 6)) #	"0xD77C-6": "Beat Celadon Gym Trainer 4",
    g4_6 = GYM_TRAINER * int(read_bit(pyboy, 0xD77C, 7)) #	"0xD77C-7": "Beat Celadon Gym Trainer 5",
    g4_7 = GYM_TRAINER * int(read_bit(pyboy, 0xD77D, 0)) #	"0xD77D-0": "Beat Celadon Gym Trainer 6",
    return sum([four, g4_1, g4_2, g4_3, g4_4, g4_5, g4_6, g4_7, ])

def gym5(pyboy):
   #gym 5 Fuchsia	
    five = GYM_LEADER * int(read_bit(pyboy, 0xD7B3, 1))
    g5_1 = GYM_TRAINER * int(read_bit(pyboy, 0xD792, 2)) #	"0xD792-2": "Beat Fuchsia Gym Trainer 0",
    g5_2 = GYM_TRAINER * int(read_bit(pyboy, 0xD792, 3)) #	"0xD792-3": "Beat Fuchsia Gym Trainer 1",
    g5_3 = GYM_TRAINER * int(read_bit(pyboy, 0xD792, 4)) #	"0xD792-4": "Beat Fuchsia Gym Trainer 2",
    g5_4 = GYM_TRAINER * int(read_bit(pyboy, 0xD792, 5)) #	"0xD792-5": "Beat Fuchsia Gym Trainer 3",
    g5_5 = GYM_TRAINER * int(read_bit(pyboy, 0xD792, 6)) #	"0xD792-6": "Beat Fuchsia Gym Trainer 4",
    g5_6 = GYM_TRAINER * int(read_bit(pyboy, 0xD792, 7)) #	"0xD792-7": "Beat Fuchsia Gym Trainer 5",
    return sum([five, g5_1, g5_2, g5_3, g5_4, g5_5, g5_6, ])

def gym6(pyboy):
   #gym 6 Saffron	
    six = GYM_LEADER * int(read_bit(pyboy, 0xD7B3, 1))
    g6_1 = GYM_TRAINER * int(read_bit(pyboy, 0xD7B3, 2)) #	"0xD7B3-2": "Beat Saffron Gym Trainer 0",
    g6_2 = GYM_TRAINER * int(read_bit(pyboy, 0xD7B3, 3)) #	"0xD7B3-3": "Beat Saffron Gym Trainer 1",
    g6_3 = GYM_TRAINER * int(read_bit(pyboy, 0xD7B3, 4)) #	"0xD7B3-4": "Beat Saffron Gym Trainer 2",
    g6_4 = GYM_TRAINER * int(read_bit(pyboy, 0xD7B3, 5)) #	"0xD7B3-5": "Beat Saffron Gym Trainer 3",
    g6_5 = GYM_TRAINER * int(read_bit(pyboy, 0xD7B3, 6)) #	"0xD7B3-6": "Beat Saffron Gym Trainer 4",
    g6_6 = GYM_TRAINER * int(read_bit(pyboy, 0xD7B3, 7)) #	"0xD7B3-7": "Beat Saffron Gym Trainer 5",
    g6_7 = GYM_TRAINER * int(read_bit(pyboy, 0xD7B4, 0)) #	"0xD7B4-0": "Beat Saffron Gym Trainer 6",
    return sum([six, g6_1, g6_2, g6_3, g6_4, g6_5, g6_6, g6_7, ])

def gym7(pyboy):
   #gym 7 Cinnabar	
    seven = GYM_LEADER * int(read_bit(pyboy, 0xD79A, 1))
    g7_1 = GYM_TRAINER * int(read_bit(pyboy, 0xD79A, 2)) #	"0xD79A-2": "Beat Cinnabar Gym Trainer 0",
    g7_2 = GYM_TRAINER * int(read_bit(pyboy, 0xD79A, 3)) #	"0xD79A-3": "Beat Cinnabar Gym Trainer 1",
    g7_3 = GYM_TRAINER * int(read_bit(pyboy, 0xD79A, 4)) #	"0xD79A-4": "Beat Cinnabar Gym Trainer 2",
    g7_4 = GYM_TRAINER * int(read_bit(pyboy, 0xD79A, 5)) #	"0xD79A-5": "Beat Cinnabar Gym Trainer 3",
    g7_5 = GYM_TRAINER * int(read_bit(pyboy, 0xD79A, 6)) #	"0xD79A-6": "Beat Cinnabar Gym Trainer 4",
    g7_6 = GYM_TRAINER * int(read_bit(pyboy, 0xD79A, 7)) #	"0xD79A-7": "Beat Cinnabar Gym Trainer 5",
    g7_7 = GYM_TRAINER * int(read_bit(pyboy, 0xD79B, 0)) #	"0xD79B-0": "Beat Cinnabar Gym Trainer 6",

    return sum([seven, g7_1, g7_2, g7_3, g7_4, g7_5, g7_6, g7_7, ])

def gym8(pyboy):
   #gym 8 Viridian	
  # "0xD74C-0": "Viridian Gym Open",
  gym_door = GYM_TASK * int(read_bit(pyboy, 0xD74C, 0))
  eight = GYM_LEADER * int(read_bit(pyboy, 0xD751, 1))
  g8_1 = GYM_TRAINER * int(read_bit(pyboy, 0xD751, 2)) #	"0xD751-2": "Beat Viridian Gym Trainer 0",
  g8_2 = GYM_TRAINER * int(read_bit(pyboy, 0xD751, 3)) #	"0xD751-3": "Beat Viridian Gym Trainer 1",
  g8_3 = GYM_TRAINER * int(read_bit(pyboy, 0xD751, 4)) #	"0xD751-4": "Beat Viridian Gym Trainer 2",
  g8_4 = GYM_TRAINER * int(read_bit(pyboy, 0xD751, 5)) #	"0xD751-5": "Beat Viridian Gym Trainer 3",
  g8_5 = GYM_TRAINER * int(read_bit(pyboy, 0xD751, 6)) #	"0xD751-6": "Beat Viridian Gym Trainer 4",
  g8_6 = GYM_TRAINER * int(read_bit(pyboy, 0xD751, 7)) #	"0xD751-7": "Beat Viridian Gym Trainer 5",
  g8_7 = GYM_TRAINER * int(read_bit(pyboy, 0xD752, 0)) #	"0xD752-0": "Beat Viridian Gym Trainer 6",
  g8_8 = GYM_TRAINER * int(read_bit(pyboy, 0xD752, 1)) #	"0xD752-1": "Beat Viridian Gym Trainer 7",
  return sum([eight, g8_1, g8_2, g8_3, g8_4, g8_5, g8_6, g8_7, g8_8, gym_door])

def rival(pyboy):
  one = RIVAL * int(read_bit(pyboy, 0xD74B, 3))
  two = RIVAL * int(read_bit(pyboy, 0xD7EB, 0))
  three = RIVAL * int(read_bit(pyboy, 0xD7EB, 1))
  four = RIVAL * int(read_bit(pyboy, 0xD7EB, 5))
  five = RIVAL * int(read_bit(pyboy, 0xD7EB, 6))
  six = RIVAL * int(read_bit(pyboy, 0xD75A, 0))
  seven = RIVAL * int(read_bit(pyboy, 0xD764, 6))
  eight = RIVAL * int(read_bit(pyboy, 0xD764, 7))
  nine = RIVAL * int(read_bit(pyboy, 0xD7EB, 7))
  Beat_Silph_Co_Rival = RIVAL * int(read_bit(pyboy, 0xD82F, 0))

  return sum([one, two, three, four, five, six, seven, eight, nine, Beat_Silph_Co_Rival])

# UTIL #####################################################################################################

def bcd(num):
    return 10 * ((num >> 4) & 0x0F) + (num & 0x0F)

def bit_count(bits):
    return bin(bits).count("1")

def read_bit(pyboy, addr, bit) -> bool:
    # add padding so zero will read '0b100000000' instead of '0b0'
    return bin(256 + pyboy.memory[addr])[-bit - 1] == "1"

def mem_val(pyboy, addr):
    mem = pyboy.memory[addr]
    return mem

def read_uint16(pyboy, start_addr):
    """Read 2 bytes"""
    val_256 = pyboy.memory[start_addr]
    val_1 = pyboy.memory[start_addr + 1]
    return 256 * val_256 + val_1

# MISC #####################################################################################################

def get_hm_count(pyboy):
    hm_ids = [0xC4, 0xC5, 0xC6, 0xC7, 0xC8]
    items = get_items_in_bag(pyboy)
    total_hm_cnt = 0
    for hm_id in hm_ids:
        if hm_id in items:
            total_hm_cnt += 1
    return total_hm_cnt * 1

def get_items_in_bag(pyboy, one_indexed=0):
    first_item = 0xD31E
    item_ids = []
    for i in range(0, 40, 2):
        item_id = pyboy.memory[first_item + i]
        if item_id == 0 or item_id == 0xff:
            break
        item_ids.append(item_id + one_indexed)
    return item_ids

def position(pyboy): # this is [y, x, z]
    r_pos = pyboy.memory[Y_POS_ADDR]
    c_pos = pyboy.memory[X_POS_ADDR]
    map_n = pyboy.memory[MAP_N_ADDR]
    if r_pos >= 443:
        r_pos = 444
    if r_pos <= 0:
        r_pos = 0
    if c_pos >= 443:
        c_pos = 444
    if c_pos <= 0:
        c_pos = 0
    if map_n > 247:
        map_n = 247
    if map_n < -1:
        map_n = -1
    return r_pos, c_pos, map_n

def party(pyboy):
    # party = [pyboy.memory[addr) for addr in PARTY_ADDR]
    party_size = pyboy.memory[PARTY_SIZE_ADDR]
    party_levels = [x for x in [pyboy.memory[addr] for addr in PARTY_LEVEL_ADDR] if x > 0]
    return party_size, party_levels # [x for x in party_levels if x > 0]

def hp(pyboy):
    """Percentage of total party HP"""
    party_hp = [read_uint16(pyboy, addr) for addr in HP_ADDR]
    party_max_hp = [read_uint16(pyboy, addr) for addr in MAX_HP_ADDR]
    # Avoid division by zero if no pokemon
    sum_max_hp = sum(party_max_hp)
    if sum_max_hp == 0:
        return 1
    return sum(party_hp) / sum_max_hp

def write_mem(pyboy, addr, value):
    mem = pyboy.set_memory_value(addr, value)
    return mem

def badges(pyboy):
    badges = pyboy.memory[BADGE_1_ADDR]
    return bit_count(badges)

def update_pokedex(pyboy):
    seen_pokemon = np.zeros(152, dtype=np.uint8)
    caught_pokemon = np.zeros(152, dtype=np.uint8)
    for i in range(0xD30A - 0xD2F7):
        caught_mem = pyboy.memory[i + 0xD2F7]
        seen_mem = pyboy.memory[i + 0xD30A]
        for j in range(8):
            caught_pokemon[8*i + j] = 1 if caught_mem & (1 << j) else 0
            seen_pokemon[8*i + j] = 1 if seen_mem & (1 << j) else 0  
    return sum(seen_pokemon), sum(caught_pokemon)

def update_moves_obtained(pyboy):
    # Scan party
    moves_obtained = {}
    cut = 0
    for i in [0xD16B, 0xD197, 0xD1C3, 0xD1EF, 0xD21B, 0xD247]:
        if pyboy.memory[i] != 0:
            for j in range(4):
                move_id = pyboy.memory[i + j + 8]
                if move_id != 0:
                    if move_id != 0:
                        moves_obtained[move_id] = 1
                    if move_id == 15:
                        cut = 1
    # Scan current box (since the box doesn't auto increment in pokemon red)
    num_moves = 4
    box_struct_length = 25 * num_moves * 2
    for i in range(pyboy.memory[0xda80]):
        offset = i*box_struct_length + 0xda96
        if pyboy.memory[offset] != 0:
            for j in range(4):
                move_id = pyboy.memory[offset + j + 8]
                if move_id != 0:
                    moves_obtained[move_id] = 1
    return sum(moves_obtained), cut

def check_if_in_start_menu(pyboy) -> bool:
    return (
        mem_val(pyboy, 0xD057) == 0
        and mem_val(pyboy, 0xCF13) == 0
        and mem_val(pyboy, 0xFF8C) == 6
        and mem_val(pyboy, 0xCF94) == 0
    )

def check_if_in_pokemon_menu(pyboy) -> bool:
    return (
        mem_val(pyboy, 0xD057) == 0
        and mem_val(pyboy, 0xCF13) == 0
        and mem_val(pyboy, 0xFF8C) == 6
        and mem_val(pyboy, 0xCF94) == 2
    )

def check_if_in_stats_menu(pyboy) -> bool:
    return (
        mem_val(pyboy, 0xD057) == 0
        and mem_val(pyboy, 0xCF13) == 0
        and mem_val(pyboy, 0xFF8C) == 6
        and mem_val(pyboy, 0xCF94) == 1
    )

def check_if_in_bag_menu(pyboy) -> bool:
    return (
        mem_val(pyboy, 0xD057) == 0
        and mem_val(pyboy, 0xCF13) == 0
        # and mem_val(pyboy, 0xFF8C) == 6 # only sometimes
        and mem_val(pyboy, 0xCF94) == 3
    )

# ##################################################################################################################
#                                                     # Notes
# ##################################################################################################################

## Misc
    # 0xc4f2 check for EE hex for text box arrow is present

## Menu Data
    # Coordinates of the position of the cursor for the top menu item (id 0)
    # CC24 : Y position
    # CC25 : X position
    # CC26 - Currently selected menu item (topmost is 0)
    # CC27 - Tile "hidden" by the menu cursor
    # CC28 - ID of the last menu item
    # CC29 - bitmask applied to the key port for the current menu
    # CC2A - ID of the previously selected menu item
    # CC2B - Last position of the cursor on the party / Bill's PC screen
    # CC2C - Last position of the cursor on the item screen
    # CC2D - Last position of the cursor on the START / battle menu
    # CC2F - Index (in party) of the Pokémon currently sent out
    # CC30~CC31 - Pointer to cursor tile in C3A0 buffer
    # CC36 - ID of the first displayed menu item
    # CC35 - Item highlighted with Select (01 = first item, 00 = no item, etc.)
    # CC3A and CC3B are unused 
    # cc51 and cc52 both read 00 when menu is closed 

## Pokémon Mart
    # JPN addr. 	INT addr. 	Description
    # CF62 	    CF7B 	    Total Items
    # CF63 	    CF7C 	    Item 1
    # CF64 	    CF7D 	    Item 2
    # CF65 	    CF7E 	    Item 3
    # CF66 	    CF7F 	    Item 4
    # CF67 	    CF80 	    Item 5
    # CF68 	    CF81 	    Item 6
    # CF69 	    CF82 	    Item 7
    # CF70 	    CF83 	    Item 8
    # CF71 	    CF84 	    Item 9
    # CF72 	    CF85 	    Item 10 

## Event Flags 
    # D751 - Fought Giovanni Yet?
    # D755 - Fought Brock Yet?
    # D75E - Fought Misty Yet?
    # D773 - Fought Lt. Surge Yet?
    # D77C - Fought Erika Yet?
    # D792 - Fought Koga Yet?
    # D79A - Fought Blaine Yet?
    # D7B3 - Fought Sabrina Yet?
    # D782 - Fought Articuno Yet?
    # D7D4 - Fought Zapdos Yet?
    # D7EE - Fought Moltres Yet?
    # D710 - Fossilized Pokémon?
    # D7D8 - Fought Snorlax Yet (Vermilion)
    # D7E0 - Fought Snorlax Yet? (Celadon)
    # D803 - Is SS Anne here
    # D5F3 - Have Town map?
    # D60D - Have Oak's Parcel?
    # D5A6 to D5C5 : Missable Objects Flags (flags for every (dis)appearing sprites, like the guard in Cerulean City or the Pokéballs in Oak's Lab)
    # D5AB - Starters Back?
    # D5C0(bit 1) - 0=Mewtwo appears, 1=Doesn't (See D85F)
    # D700 - Bike Speed
    # D70B - Fly Anywhere Byte 1
    # D70C - Fly Anywhere Byte 2
    # D70D - Safari Zone Time Byte 1
    # D70E - Safari Zone Time Byte 2
    # D714 - Position in Air
    # D72E - Did you get Lapras Yet?
    # D732 - Debug New Game
    # D790 - If bit 7 is set, Safari Game over
    # D85F - Mewtwo can be caught if bit 2 clear - Needs D5C0 bit 1 clear, too 

## Item IDs & String
    # 1, 2, 3, 4, 6, 11, 16, 17, 18, 19, 20, 41, 42, 72, 73, 196, 197, 198, 199, 200, 53, 54
    # 001 	0x01 	Master Ball
    # 002 	0x02 	Ultra Ball
    # 003 	0x03 	Great Ball
    # 004 	0x04 	Poké Ball
    # 006 	0x06 	Bicycle
    # 011 	0x0B 	Antidote
    # 016 	0x10 	Full Restore
    # 017 	0x11 	Max Potion
    # 018 	0x12 	Hyper Potion
    # 019 	0x13 	Super Potion
    # 020 	0x14 	Potion
    # 041 	0x29 	Dome Fossil
    # 042 	0x2A 	Helix Fossil
    # 072 	0x48 	Silph Scope
    # 073 	0x49 	Poké Flute
    # 196 	0xC4 	HM01
    # 197 	0xC5 	HM02
    # 198 	0xC6 	HM03
    # 199 	0xC7 	HM04
    # 200 	0xC8 	HM05
    # 053 	0x35 	Revive
    # 054 	0x36 	Max Revive