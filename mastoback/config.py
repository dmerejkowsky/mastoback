import os
from typing import Any, Dict, NewType

from path import Path
import ruamel.yaml


CFG_PATH = os.path.expanduser("~/.config/mastoback.yml")

Config = NewType('Config', Dict[str, Any])


def read_config() -> Config:
    conf_path = Path(CFG_PATH)
    parsed: Config = ruamel.yaml.safe_load(conf_path.text())
    return parsed
