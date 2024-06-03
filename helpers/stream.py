import asyncio
import websockets
import json
import gymnasium as gym
from helpers import calc_reward

X_POS_ADDRESS, Y_POS_ADDRESS = 0xD362, 0xD361
MAP_N_ADDRESS = 0xD35E

class StreamWrapper(gym.Wrapper):
    def __init__(self, env, stream_metadata={}):
        super().__init__(env)
        self.ws_address = "wss://transdimensional.xyz/broadcast"
        self.stream_metadata = stream_metadata
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.websocket = None
        self.loop.run_until_complete(
            self.establish_wc_connection()
        )
        self.upload_interval = 100
        self.steam_step_counter = 0
        self.coord_list = []
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

        if self.steam_step_counter >= self.upload_interval:

            extra = str("RW: " + str(round(self.env.rewardtotal,2)) + "\n" + "LVL: " + str(self.env.pokelvlsumtrack) + "\n" + "BADGE: " + str(self.env.badges))    

            self.stream_metadata["extra"] = extra
            try:
                metadata_serializable = {k: v for k, v in self.stream_metadata.items() if isinstance(v, (str, int, float, list, dict))}
                message = json.dumps({
                    "metadata": metadata_serializable,
                    "coords": self.coord_list
                })
                self.loop.run_until_complete(self.broadcast_ws_message(message))
            except TypeError as e:
                print(f"Serialization error: {e}")
            
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