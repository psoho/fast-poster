import sys, getopt
import os
import random

keys = dict()

KEYS_FILE_NAME = "keys.txt"
seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def load_keys():
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
    if not accessKey:
        return False
    if not secretKey:
        return False
    return accessKey in keys and keys[accessKey] == secretKey


def save_keys(keys):
    with open(KEYS_FILE_NAME, mode='w') as f:
        f.writelines(keys)


def rkey(len=16, seed=seed):
    sa = []
    for i in range(len):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def init():
    help_info = """fast.py -k <accessKey> -s <secretKey>"""
    if load_keys():
        return
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
        save_keys([f"{accessKey} {secretKey}"])
        load_keys()
