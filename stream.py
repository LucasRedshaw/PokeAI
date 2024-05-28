import asyncio
import websockets
import json

import gymnasium as gym
from data import poke_dict

#colors
BLUE = "#0000FF"
GREEN = "#00A36C"
RED = "#FF0000"
PURPLE = "#800080"
PINK = "#FF00FF"
YELLOW = "#DAEE01"

POKE = [0xD16B, 0xD197, 0xD1C3, 0xD1EF, 0xD21B, 0xD247]
LEVEL = [0xD18C, 0xD1B8, 0xD1E4, 0xD210, 0xD23C, 0xD268]
X_POS_ADDRESS, Y_POS_ADDRESS = 0xD362, 0xD361
MAP_N_ADDRESS = 0xD35E

class StreamWrapper(gym.Wrapper):
    def __init__(self, env, stream_metadata={}):
        super().__init__(env)
        self.ws_address = "wss://transdimensional.xyz/broadcast" # "ws://theleanke.com/broadcast"
        self.stream_metadata = stream_metadata
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.websocket = self.loop.run_until_complete(
                self.establish_wc_connection()
        )
        self.upload_interval = 250
        self.steam_step_counter = 0
        self.env = env
        self.coord_list = []
        self.leanke = {}
        self.cut = 0

        if hasattr(env, "pyboy"):
            self.emulator = env.pyboy
        elif hasattr(env, "game"):
            self.emulator = env.game
        else:
            raise Exception("Could not find emulator!")


    def step(self, action):

        x_pos = self.emulator.memory[X_POS_ADDRESS]
        y_pos = self.emulator.memory[Y_POS_ADDRESS]
        map_n = self.emulator.memory[MAP_N_ADDRESS]
        self.coord_list.append([x_pos, y_pos, map_n])

        poke0 = self.emulator.memory[POKE[0]]
        lvl0 = self.emulator.memory[LEVEL[0]]
        name_info6 = poke_dict.get(poke0, {})
        name0 = name_info6.get("name", "")

        if self.steam_step_counter >= self.upload_interval:

            self.stream_metadata['color'] = PURPLE
            self.stream_metadata['extra'] = f"{name0}: {lvl0}"

            self.loop.run_until_complete(
                self.broadcast_ws_message(
                    json.dumps(
                        {
                            "metadata": self.stream_metadata,
                            "coords": self.coord_list,
                            })))
            
            self.steam_step_counter = 0
            self.coord_list = []

        self.steam_step_counter += 1

        return self.env.step(action)

    async def broadcast_ws_message(self, message):
        if self.websocket is None:
            await self.establish_wc_connection()
        if self.websocket is not None:
            try:
                await self.websocket.send(message)
            except websockets.exceptions.WebSocketException as e:
                self.websocket = None

    async def establish_wc_connection(self):
        try:
            self.websocket = await websockets.connect(self.ws_address)
        except:
            self.websocket = None
