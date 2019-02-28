import yaml
from pathlib import Path

__config = None


def config():
    global __config
    if not __config:
        path = Path('scrapper/config/config.yaml')
        with open(path, mode='r') as file:
            __config = yaml.load(file)

    return __config


def str_slug(string):
    return string.lower().strip() \
        .replace(".", "") \
        .replace("$", "") \
        .replace(" ", "-") \
        .replace("á", "a") \
        .replace("é", "e") \
        .replace("í", "i") \
        .replace("ó", "o") \
        .replace("ú", "u") \
        .replace("\"", "")
