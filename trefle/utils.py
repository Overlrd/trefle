from typing import Callable
from exceptions import TrefleException

import configparser
config = configparser.ConfigParser()

def write_token(token):
    # write the token to a keys.ini file
    config['DEFAULT'] = {"token": token}
    with open('keys.ini', 'w') as configfile:
        config.write(configfile)

def get_token(callback: Callable = None):
    # read the token from the keys.ini
    config.read('keys.ini')
    try:
        t = config['DEFAULT']['token']
    except KeyError:
        return callback()
    else:
        return t
