import json


class R():
    """
    响应实体
    """

    def __init__(self, code=0):
        self.d = {'code': code, 'msg': ''}

    def json(self):
        """
        返回json数据
        :return:
        """
        return json.dumps(self.d)

    def dict(self):
        # 返回字典
        return self.d

    def add(self, key, value):
        """
        链式调用支持
        :param key:
        :param value:
        :return:
        """
        self.d[key] = value
        return self

    def __str__(self):
        """
        string处理
        """
        self.json()


def ok(msg='操作成功'):
    return R().add('msg', msg)


def error(msg='操作失败'):
    return R(400).add('msg', msg)


def expire(msg='token失效'):
    return R(401).add('msg', msg)


if __name__ == '__main__':
    print(ok('操作成功').json())
