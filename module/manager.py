import time

from .bombScreen import BombScreen, Hero, Login
from .logger import logger
from .mouse import *
from .utils import *
from .window import get_windows
from .config import Config


def create_bombcrypto_managers():
    return [BombcryptoManager(w) for w in get_windows()]


class BombcryptoManager:
    def __init__(self, window) -> None:
        self.window = window
        self.refresh_login = now() + Config.get('screen', 'refresh_login')*60
        self.refresh_heroes = 0
        self.refresh_hunt = 0
        self.refresh_print_chest = 0

    def __enter__(self):
        self.window.activate()
        time.sleep(2)
        return self

    def __exit__(self, type, value, tb):
        return

    def do_what_needs_to_be_done(self):
            
        refresh_heroes=Config.get('screen', 'refresh_heroes')*60
        if (refresh_heroes and (now() - self.refresh_heroes > refresh_heroes)):
            Hero.who_needs_work(self)

        refresh_hunt = Config.get('screen', 'refresh_hunt')*60
        if (refresh_hunt and (now() - self.refresh_hunt > refresh_hunt)):
            Hero.refresh_hunt(self)

        refresh_login = Config.get('screen', 'refresh_login')*60
        if (refresh_login and (now() - self.refresh_login > refresh_login)):
            Login.do_login(self)
        
        if Config.get('telegram','token') and  Config.get('telegram','chat_id'):
            refresh_print_chest = Config.get('telegram', 'refresh_print_chest')*60
            if (refresh_print_chest and (now() - self.refresh_print_chest > refresh_print_chest)):
                BombScreen.do_print_chest(self)
        
        return True
  
    def set_logged(self, logged):
        self.logged = logged
        if logged:
            self.refresh_login = time.time()

    def set_positions_refreshed(self):
        self.refresh_hunt = time.time()
    
    def set_heroes_refreshed(self):
        self.refresh_heroes = time.time()
    
    def set_print_chest_refreshed(self):
        self.refresh_print_chest = time.time()

