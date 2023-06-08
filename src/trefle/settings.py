import json

from appdirs import AppDirs
from pathlib import Path

__settings = {
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

_dirs = AppDirs("trefle", "overlrd")
_DATA_DIR = Path(_dirs.user_data_dir)
_API_SETTINGS = "api_settings.json"
_API_SETTINGS_PATH = Path(_DATA_DIR) / _API_SETTINGS

if not _DATA_DIR.exists():
    Path.mkdir(_DATA_DIR, exist_ok=True)

if not _API_SETTINGS_PATH.is_file():
    with open(_API_SETTINGS_PATH, "a+") as f:
        json.dump(__settings, f)

Paths = dict(
    api_settings=_API_SETTINGS_PATH,
)
