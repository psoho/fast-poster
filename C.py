import hashlib
import json
import os
import uuid

# 总存储目录
STORE = 'static/storage'

# 上传文件存储目录
STORE_UPLOAD = STORE + '/upload'

# 预览文件存储目录
STORE_PREVIEW = STORE + '/preview/'

# 数据文件存放目录
STORE_DB = 'db'

# 状态常量
STATUS_NORMAL = 1  # 正常
STATUS_DELETE = 2  # 删除


def mkdirs(path):
    if not os.path.exists(path):
        print("目录是否存在(不存在-创建目录): path=" + path)
        os.makedirs(path)
    # else:
    # print("已存在: path=" + path)


def init_path():
    """
    初始化路径
    :return:
    """
    print("初始化路径")
    mkdirs(STORE_DB)
    mkdirs(STORE_PREVIEW)
    mkdirs(STORE_UPLOAD)


def add_url_prefix(path: str):
    """
    增加URL前缀
    :param path:
    :return:
    """
    if path and path.startswith('http'):
        return path
    if path.startswith("/"):
        path = path[1:]
    prefix = os.environ.get('POSTER_URI_PREFIX', '')
    if prefix and not prefix.endswith("/"):
        prefix += "/"
    return prefix + path


def get_url_path(path: str):
    """
    获取资源的URL访问路径
    :param path:
    :return:
    """
    return add_url_prefix(path.replace('static/', ''))


def get_url_local_path(url):
    """
    获得资源的本地存储路径
    :param url:
    :return:
    """
    return 'static' + url


def md5(param: str, len=32) -> str:
    """
    计算对象或者字符串的MD5值
    @param param:
    @return:
    """
    if type(param) != 'str':
        param = json.dumps(param)
    return hashlib.md5(param.encode()).hexdigest()[0:len]


def code(len=32) -> str:
    """
    生成指定长度的随机数
    @param len:
    @return:
    """
    return md5(str(uuid.uuid4()), len)
