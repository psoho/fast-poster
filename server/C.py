import datetime
import hashlib
import json
import os
import uuid
import yaml

STORE_DB = 'data/db'
STORE_DIR = 'data/store'
STATUS_NORMAL = 1
STATUS_DELETE = 2

config = {}
if os.path.exists('app.yml'):
    config = yaml.safe_load(open('app.yml'))


def mkdirs(path):
    if not os.path.exists(path):
        print("mkdirs: path=" + path)
        os.makedirs(path)
    return path


def init_path():
    mkdirs(STORE_DB)


def md5(param: str, len=32) -> str:
    if type(param) != 'str':
        param = json.dumps(param)
    return hashlib.md5(param.encode()).hexdigest()[0:len]


def code(len=32) -> str:
    return md5(str(uuid.uuid4()), len)


def indocker():
    return os.environ.get('FASTPOSTER_IN_DOCKER', None) is not None
