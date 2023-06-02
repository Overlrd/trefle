import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

class URLs:
    """
    This class contains the urls of all the routes of the trefle API
    """
    def __init__(self, version: str = 'v1', settings_path: str = "api_settings.json"):
        self.api_version = version
        self.settings_path = settings_path
        self.base_url = None
        self.parse_settings()

    def parse_settings(self):
        assert Path(self.settings_path).is_file()
        json_settings = open(self.settings_path, "r")
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

"""
settings = {
    "title": "Trefle API v1",
    "version": "1.6.0",
    "url": "https://trefle.io/api/{version}",
    "paths": {
        "listKingdoms": {"method": "get", "path": "/kingdoms", "params": ["page"]},
        "getKingdom": {"method": "get", "path": "/kingdoms/{id}", "params": ["id-required"]},

        "listSubkingdoms": {"method": "get", "path": "/subkingdoms", "params": ["page"]},
        "getSubkingdom": {"method": "get", "path": "/subkingdoms/{id}", "params": ["id-required"]},

        "listDivisions": {"method": "get", "path": "/divisions", "params": ["page"]},
        "getDivision": {"method": "get", "path": "/divisions/{id}", "params": ["id-required"]},

        "listDivisionClasses": {"method": "get", "path": "/division_classes", "params": ["page"]},
        "getDivisionClass": {"method": "get", "path": "/division_classes{id}", "params": ["id-required"]},

        "listDivisionOrders": {"method": "get", "path": "/division_orders", "params": ["page"]},
        "getDivisionOrder": {"method": "get", "path": "/division_orders/{id}", "params": ["id-required"]},

        "listFamilies": {"method": "get", "path": "/families", "params": ["page"]},
        "getFamily": {"method": "get", "path": "/families/{id}", "params": ["id-required"]},

        "listGenus": {"method": "get", "path": "/genus", "params": ["page", "filter", "order"]},
        "getGenus": {"method": "get", "path": "/genus/{id}", "params": ["id-required"]},

        "listPlants": {"method": "get", "path": "/plants", "params": ["page", "range", "order", "filter_not",
                                                                      "filter"]},
        "getPlant": {"method": "get", "path": "/plants/{id}", "params": ["id-required"]},
        "searchPlants": {"method": "get", "path": "/plants/search",
                         "params": ["page", "range", "order", "filter_not", "filter", "q-required"]},
        "reportPlants": {"method": "post", "path": "/plants/{id}/report", "params": ["id-required", "notes"]},
        "listPlantsZone": {"method": "get", "path": "/distributions/{zone_id}/plants",
                           "params": ["page", "zone_id-required", "range", "order", "filter_not", "filter"]},
        "listPlantsGenus": {"method": "get", "path": "/genus/{genus_id}/plants",
                            "params": ["page", "genus_id-required", "range", "order", "filter_not", "filter"]},

        "listSpecies": {"method": "get", "path": "/species", "params": ["page", "range", "order",
                                                                        "filter_not", "filter"]},
        "getSpecies": {"method": "get", "path": "/species/{id}", "params": ["id-required"]},
        "searchSpecies": {"method": "get", "path": "/species/search", "params": ["page", "range", "order",
                                                                                 "filter_not", "filter",
                                                                                 "q-required"]},

        "reportSpecies": {"method": "post", "path": "/species/{id}/report",
                          "params": ["id-required", "notes"]},

        "listDistributions": {"method": "get", "path": "/distributions", "params": ["page"]},
        "getZone": {"method": "get", "path": "/distributions/{id}", "params": ["id-required"]},

        "claimClientSideToken": {"method": "post", "path": "/auth/claim",
                                 "params": ["origin-required", "ip"]},

        "listCorrections": {"method": "get", "path": "/corrections", "params": []},
        "getCorrection": {"method": "get", "path": "/corrections/{id}", "params": ["id-required"]},
        "createCorrection": {"method": "post", "path": "/corrections/species/{record_id}",
                             "params": ["record_id-required", "notes", "source_type", "source_reference",
                                        "correction"]},
    },
}
 """
