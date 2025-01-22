from Window import Window
from ConfigLoader import ConfigLoader
import os

config_file_informations = {
    "settings":
        {
            'items':{
                'full_screen':'bool',
                'sound_on':'bool',
                'dev_mode':'bool',
                'screen_size':'other',
                'game_server_host':'str',
                'game_server_port':'int',
            }
        },
}
CONFIGURATIONS = ConfigLoader.Load(f"{os.getcwd()}/Bomberman/config.ini", config_file_informations) # Load all configurations
GAME_CONFIGURATIONS = CONFIGURATIONS['settings']['items'] # Load settings section from configuratios for game

GMSERVER = (GAME_CONFIGURATIONS['game_server_host'], # HOST
            GAME_CONFIGURATIONS['game_server_port']) # PORT

window = Window(GAME_CONFIGURATIONS['screen_size'][0],GAME_CONFIGURATIONS['screen_size'][1],"2D Runner",dev_mode=GAME_CONFIGURATIONS['dev_mode'],fullscreen=GAME_CONFIGURATIONS['full_screen'], sound=GAME_CONFIGURATIONS['sound_on'], server=GMSERVER)
window.start()
while True:
    if window.reload:
        window = Window(window.screen_size[0],window.screen_size[1],"2D Runner",dev_mode=GAME_CONFIGURATIONS['dev_mode'],fullscreen=window.fullscreen, sound=window.sound, server=GMSERVER)
        window.start()
    else:
        break

