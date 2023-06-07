from typing import Callable
from pathlib import Path
import configparser
from .settings import Paths
from .exceptions import TrefleException

config = configparser.ConfigParser()

keys_path = Paths["keys"]

def write_token(token):
    # write the token to a keys.ini file
    config['DEFAULT'] = {"token": token}
    with open(keys_path, 'w') as configfile:
        config.write(configfile)

def get_token(callback: Callable = None):
    # read the token from the keys.ini
    config.read(keys_path)
    try:
        t = config['DEFAULT']['token']
    except KeyError:
        return callback()
    else:
        return t
