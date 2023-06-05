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


class Q:
    FIELDS_PARAMS = {"q": "",
                     "page": "",
                     "filter": [],
                     "filter_not": [],
                     "order": [],
                     "range": []}

    def __init__(self, fields_params: Dict = FIELDS_PARAMS, **kwargs) -> None:
        self.param_fields = fields_params
        self.data = kwargs

    def check(self):
        data = self.data
        for key in data:
            if key in self.param_fields:
                pass
            else:
                raise Exception(f"{key} out of expected values")
        return data
