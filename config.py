import os
from path import Path
import ruamel.yaml

CFG_PATH = os.path.expanduser("~/.config/mastoback.yml")


def read_config():
    conf_path = Path(CFG_PATH)
    return ruamel.yaml.safe_load(conf_path.text())
