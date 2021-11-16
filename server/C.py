import datetime
import hashlib
import json
import os
import uuid

STORE_DB = 'data/db'
STORE_UPLOAD = 'data/store/upload/'
STORE_PREVIEW = 'data/store/preview/'
STATUS_NORMAL = 1
STATUS_DELETE = 2


def mkdirs(path):
    if not os.path.exists(path):
        print("mkdirs: path=" + path)
        os.makedirs(path)
    return path


def mkdirs_day(path):
    day = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    return mkdirs(f'{path}{day}')


def init_path():
    mkdirs(STORE_DB)
    mkdirs(STORE_PREVIEW)
    mkdirs(STORE_UPLOAD)


def add_url_prefix(path: str):
    if path and path.startswith('http'):
        return path
    prefix = os.environ.get('POSTER_URI_PREFIX')
    if prefix and not prefix.endswith("/"):
        prefix += "/"
    return prefix + path


def get_url_path(path: str):
    return path.replace('data/store/', 'store/')


def md5(param: str, len=32) -> str:
    if type(param) != 'str':
        param = json.dumps(param)
    return hashlib.md5(param.encode()).hexdigest()[0:len]


def code(len=32) -> str:
    return md5(str(uuid.uuid4()), len)


def get_upload_dir():
    return STORE_UPLOAD


def indocker():
    return os.environ.get('FASTPOSTER_IN_DOCKER', None) is not None
