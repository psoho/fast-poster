import datetime
import json

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class R():
    def __init__(self, code=0):
        self.d = {'code': code, 'msg': '', 'data': {}}

    def json(self):
        return json.dumps(self.d, ensure_ascii=False, cls=DateEncoder)

    def set(self, key, value):
        self.d[key] = value
        return self

    def add(self, key, value):
        self.d['data'][key] = value
        return self

    def __str__(self):
        return self.json()


def ok(msg='success'):
    return R().set('msg', msg)


def error(msg='failure'):
    return R(400).set('msg', msg)


def expire(msg='token expired'):
    return R(401).set('msg', msg)


if __name__ == '__main__':
    print(ok('操作成功'))
