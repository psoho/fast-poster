import json


class R():
    def __init__(self, code=0):
        self.d = {'code': code, 'msg': ''}

    def json(self):
        return json.dumps(self.d, ensure_ascii=False)

    def add(self, key, value):
        self.d[key] = value
        return self

    def __str__(self):
        self.json()


def ok(msg='success.'):
    return R().add('msg', msg)


def error(msg='failure!'):
    return R(400).add('msg', msg)


def expire(msg='token expired.'):
    return R(401).add('msg', msg)


if __name__ == '__main__':
    print(ok('操作成功').json())
