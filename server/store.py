import os

import C

def save_to_disc(filename, content_type, body):
    """
    存储文件到磁盘
    :param filename:
    :param content_type:
    :param body:
    :return:
    """
    name, ext = os.path.splitext(filename)
    name = C.get_upload_dir() + '/' + C.code(16) + ext
    with open(name, mode='bw') as f:
        f.write(body)
    return C.get_url_path(name)


def uploads(files):
    items = []
    for field_name, files in files.items():
        for info in files:
            filename, content_type = info["filename"], info["content_type"]
            body = info["body"]
            url = save_to_disc(filename, content_type, body)
            items.append(url)
    return items
