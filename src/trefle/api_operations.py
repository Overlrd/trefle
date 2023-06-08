import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
from .settings import Paths

class APIRoutes:
    """
    This class contains the available operations , their urls
    and their parameters of the trefle API
    """
    def __init__(self, version: str = 'v1'):
        self.api_version = version
        self.base_url = None
        self.parse_settings()

    def parse_settings(self):
        settings_path = Paths['api_settings']
        assert settings_path.is_file()
        json_settings = open(settings_path, "r")
        settings = json.load(json_settings)

        url = settings['url'].format(version=self.api_version)
        setattr(self, 'base_url', url)

        paths = settings['paths']
        for i in paths:
            path = paths[i]
            path['path'] = ''.join([self.base_url, path['path']])
            path_obj = APIPath(**path)
            setattr(self, i, path_obj)


@dataclass
class APIPath:
    method: str
    path: str
    params: Optional[List]