import asyncio
import sys
import time
from pygame import mixer
from gtts import gTTS
from io import BytesIO
from typing import List, ClassVar, Mapping, Optional

from viam.components.generic import Generic
from viam.components.component_base import ValueTypes
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Geometry
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.logging import getLogger


class SoundPlayer(Generic):
    MODEL: ClassVar[Model] = Model(ModelFamily("jeremyrhyde", "generic"), "play-sound")

    LOGGER = getLogger(__name__)

    mixer.init()
    mixer.music.set_volume(1.0)

    possible_keys = ["stop", "message", "file"]

    # Constructor for play-sound model
    @classmethod
    def new(cls, config: ComponentConfig,
            dependencies: Mapping[ResourceName, ResourceBase]):
        soundPlayerInstance = cls(config.name)
        soundPlayerInstance.reconfigure(config, dependencies)

        return soundPlayerInstance

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        return

    @classmethod
    # Reconfigure module by resetting the music buffer
    def reconfigure(self, config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]):
        mixer.music.unload()

        return

    @classmethod
    # Implements the do_command which will respond to a map with keys "file" or "message"
    async def do_command(self, input: Mapping[str, ValueTypes], *,
                         timeout: Optional[float] = None,
                         **kwargs) -> Mapping[str, ValueTypes]:
        

        # Check for valid request
        valid_key = False
        for key in self.possible_keys:
            if key in input.keys():
                valid_key = True

        if (not valid_key):
            self.LOGGER.warn("no valid input, please use commands 'message' or 'file'")
            return {"response": "invalid request, no valid command given"}

        # Play message
        if "message" in input.keys():
            self.LOGGER.info("Playing message \'" + input["message"] + "\'")
            await self.play_message(self, input["message"])

        # Play audio file
        if "file" in input.keys():
            self.LOGGER.info("Playing " + input["file"])
            await self.play_audio_file(self, input["file"])

        if "stop" in input.keys():
            await self.stop(self)

        resp = {}
        return resp
    
    @classmethod
    async def get_geometries(self) -> List[Geometry]:
        return 
    
    @classmethod
    async def close(self) -> None:
        await self.stop(self)
        return 
    
    async def stop(self):
        mixer.music.stop()
        mixer.music.unload()
  
    async def play_message(self, message):
        # Stop and reset
        await self.stop(self)

        # Create audio buffer
        tts = gTTS(text=message, lang='en')
        mp3 = BytesIO()
        tts.write_to_fp(mp3)
        mp3.seek(0)

        # Play message
        mixer.music.load(mp3)
        mixer.music.play()

    async def play_audio_file(self, filename):
        # Stop and reset
        await self.stop(self)

        # Play file
        mixer.music.load(filename)
        mixer.music.play()


async def main():
    my_sound_player = SoundPlayer(name="test")

    user_command = input("Enter new do command to run (\'message\' or \'file\' or q for quit): ")
    while user_command != "q":
        if user_command not in my_sound_player.possible_keys:
            print("invalid key, try again")
        else:
            command_input = input("Enter text or path to play: ")
            request = {user_command: command_input}

            resp = await my_sound_player.do_command(request)
            print(resp)

        user_command = input("Enter new do command to run (\'message\' or \'file\' or q for quit): ")

    sys.exit()

if __name__ == '__main__':
    #main()
    asyncio.run(main())
