import sys, getopt
import os
import random

keys = dict()

KEYS_FILE_NAME = "keys.txt"
seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def load_keys():
    """
    加载KEY列表
    @return:
    """
    # print(f'load keys from file: {KEYS_FILE_NAME}')
    if not os.path.exists(KEYS_FILE_NAME):
        return False
    with open(KEYS_FILE_NAME) as f:
        for line in f:
            line = line.strip()
            kv = line.split(" ")
            keys[kv[0]] = kv[1]
        print(f"load keys is done. {keys}")
    return True


def check(accessKey, secretKey):
    """
    检查校验key是否正确
    @param accessKey:
    @param secretKey:
    @return:
    """
    # print('keys:', keys)
    if not accessKey:
        return False
    if not secretKey:
        return False
    return accessKey in keys and keys[accessKey] == secretKey


def save_keys(keys):
    """
    保存key列表
    @param keys:
    @return:
    """
    # print(f'save keys: {keys}')
    with open(KEYS_FILE_NAME, mode='w') as f:
        f.writelines(keys)


def rkey(len=16, seed=seed):
    """
    返回随机字符串
    @param len:
    @param seed:
    @return:
    """
    sa = []
    for i in range(len):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def init():
    help_info = """app.py -k <accessKey> -s <secretKey>"""
    if load_keys():
        return
    # 从参数中获取
    argv = sys.argv[1:]
    accessKey = None
    secretKey = None
    # print(f'args: {sys.argv}')
    try:
        opts, args = getopt.getopt(argv, "hk:s:", ["accessKey=", "secretKey="])
    except getopt.GetoptError:
        print(help_info)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_info)
            sys.exit()
        elif opt in ("-k", "--accessKey"):
            accessKey = arg
        elif opt in ("-s", "--secretKey"):
            secretKey = arg
    # print(f'set the keys: accessKey={accessKey}, secretKey={secretKey}')
    if accessKey and secretKey:
        # 保存传进来的key列表
        save_keys([f"{accessKey} {secretKey}"])
        # 需要重新加载一次，否则第一次无法认证
        load_keys()


# init()
