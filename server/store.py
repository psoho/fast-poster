import os
from datetime import datetime

import C


class DiskStore():
    """
    本地存储
    """

    def save(self, body, path):
        path = f'{C.STORE_DIR}/{path}'
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, mode='bw') as f:
            f.write(body)
        return path.replace('data/', '')


def save(body, filename, target='upload', rename=True):
    name = f'{C.code()}{os.path.splitext(filename)[1]}' if rename else filename
    day = datetime.strftime(datetime.now(), '%Y%m%d')
    path = f'{target}/{day}/{name}'
    return DiskStore().save(body, path)
