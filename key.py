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
    if not os.path.exists(KEYS_FILE_NAME):
        return False
    with open(KEYS_FILE_NAME) as f:
        for line in f:
            line = line.strip()
            kv = line.split(" ")
            keys[kv[0]] = kv[1]
        print(f"加载keys列表: {keys}")
    return True


def check(accessKey, secretKey):
    """
    检查校验key是否正确
    @param accessKey:
    @param secretKey:
    @return:
    """
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
    with open(KEYS_FILE_NAME, mode='w') as f:
        f.writelines(keys)


def gen_keys(times=1):
    """
    生成建列表
    @return:
    """
    keys = []
    print("生成KEY列表")
    for i in range(times):
        k = rkey()
        v = rkey(20)
        print(f"accessKey: {k}")
        print(f"secretKey: {v}\n")
        keys.append(f"{k} {v}\n")
    save_keys(keys)


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
    if accessKey and secretKey:
        # 保存传进来的key列表
        save_keys([f"{accessKey} {secretKey}"])
    else:
        # 自动生成key列表
        gen_keys()

init()