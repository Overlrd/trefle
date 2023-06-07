from appdirs import AppDirs
from pathlib import Path

_dirs = AppDirs("trefle", "overlrd")
_DATA_DIR = Path(_dirs.user_data_dir)
_API_SETTINGS = "api_settings.json"
_API_SETTINGS_PATH = Path(_DATA_DIR) / _API_SETTINGS
_KEYS = "keys.ini"
_KEYS_PATH = Path(_DATA_DIR) / _KEYS

Paths = dict(
    api_settings=_API_SETTINGS_PATH,
    keys=_KEYS_PATH
)
