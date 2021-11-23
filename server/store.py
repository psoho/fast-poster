import os

import C

def save_to_disc(filename, content_type, body):
    name, ext = os.path.splitext(filename)
    dir = C.mkdirs_day(C.STORE_UPLOAD)
    path = f'{dir}/{C.code(16)}{ext}'
    with open(path, mode='bw') as f:
        f.write(body)
    return C.get_url_path(path)


def uploads(files):
    items = []
    for field_name, files in files.items():
        for info in files:
            filename, content_type = info["filename"], info["content_type"]
            body = info["body"]
            url = save_to_disc(filename, content_type, body)
            items.append(url)
    return items
