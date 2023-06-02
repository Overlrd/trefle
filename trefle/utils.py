"""_summary_
"""
from typing import Callable, Optional, List, Dict
from exceptions import TrefleException

import configparser
config = configparser.ConfigParser()

def write_token(token):
    config['DEFAULT'] = {"token": token}
    with open('keys.ini', 'w') as configfile:
        config.write(configfile)

def get_token(callback: Callable = None):
    config.read('keys.ini')
    try:
        t = config['DEFAULT']['token']
    except KeyError:
        return callback()
    else:
        return t