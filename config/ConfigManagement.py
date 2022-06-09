import importlib
import json
import os
import uuid
from pathlib import Path

from config.Config import ConnectionConfig, Config

DATA_FOLDER = os.getcwd() + "/data/"

if not Path(DATA_FOLDER).is_dir():
    os.mkdir(DATA_FOLDER)


def retrieve_config_by_type(uid: int, type) -> list[Config]:
    if type is not str:
        type = type.__name__

    file = Path(os.path.join(
        DATA_FOLDER, (str(uid) + ".json")
    ))

    if not file.is_file():
        return []

    curr = []
    kmodule = importlib.import_module("config.Config")
    kclass = getattr(kmodule, type)

    for fat in json.loads(file.read_text()):
        if fat["type"] == type:
            curr.append(
                kclass(**fat["data"])
            )

    return curr


def remove_config_by_id(uid: int, config_id: str):
    file = Path(os.path.join(
        DATA_FOLDER, (str(uid) + ".json")
    ))
    if not file.is_file():
        return

    curr = []
    for fat in json.loads(file.read_text()):
        if not (fat["data"]["config_id"] == config_id):
            curr.append(fat)

    file.write_text(json.dumps(curr))



def save_config(uid: int, config: Config):
    file = Path(os.path.join(
        DATA_FOLDER, (str(uid) + ".json")
    ))
    config.config_id = str(uuid.uuid4())

    curr = []
    if file.is_file():
        curr = json.loads(Path.read_text(file))
    else:
        curr = []

    curr.insert(0, {
        "type": config.__class__.__name__,
        "data": config.dict()
    })

    file.write_text(json.dumps(curr))
