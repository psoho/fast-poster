import datetime
import json
import sqlite3

import C
import poster
import R


def conn():
    """
    获取数据库连接
    :return:
    """
    return sqlite3.connect(C.STORE_DB + '/poster.sqlite')


def init():
    """
    初始化数据库文件
    :return:
    """
    C.init_path()
    with conn() as con:
        c = con.cursor()

        # 判断海报表是否存在
        r = c.execute(f"select count(1) from sqlite_master where tbl_name = 'posters'")
        if r.fetchone()[0] == 0:
            c.execute('''CREATE TABLE posters (
                      id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                      code text,
                      name text,
                      preview text,
                      json text,
                      create_time date,
                      update_time date,
                      status integer
                    )''')
            print("posters created successfully.")

        # 判断分享表是否存在
        r = c.execute(f"select count(1) from sqlite_master where tbl_name = 'shares'")
        if r.fetchone()[0] == 0:
            c.execute('''CREATE TABLE shares (
                          id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                          code text,
                          pid integer,
                          params text,
                          create_time date
                        )''')
            print("shares created successfully.")

        # 判断token表是否存在
        r = c.execute(f"select count(1) from sqlite_master where tbl_name = 'tokens'")
        if r.fetchone()[0] == 0:
            c.execute('''CREATE TABLE tokens (
                          id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                          token text,
                          create_time date,
                          expire_time date
                        )''')
            print("tokens created successfully.")


# 执行初始化
init()


def db_save_poster(code: str, name: str, preview: str, json: str):
    """
    保存海报
    :param code:
    :param name:
    :param preview:
    :param json:
    :return:
    """
    with conn() as con:
        c = con.cursor()
        params = [code, name, preview, json, now_str(), int(C.STATUS_NORMAL)]
        c.execute("insert into posters (code, name, preview, json, create_time, status) values (?, ?, ?, ?, ?, ?)",
                  params)
        con.commit()
        return c.lastrowid


def db_update_poster(id: int, code: str, name: str, preview: str, json: str):
    """
    更新海报
    :param id:
    :param code:
    :param name:
    :param preview:
    :param json:
    :return:
    """
    with conn() as con:
        c = con.cursor()
        params = [code, name, preview, json, now_str(), id]
        c.execute("update posters set code=?,name=?,preview=?,json=?,update_time=? where id=?", params)
        con.commit()


def db_delete_poster(id: int):
    with conn() as con:
        c = con.cursor()
        params = [C.STATUS_DELETE, id]
        c.execute("update posters set status=? where id=?", params)
        con.commit()


def db_save_share(code, poster_id, param):
    """保存分享记录"""
    with conn() as con:
        c = con.cursor()
        params = [code, poster_id, param, now_str()]
        c.execute("insert into shares (code, pid, params, create_time) values (?, ?, ?, ?)", params)
        con.commit()
        return c.lastrowid


def query_user_posters():
    """查找用户所有海报"""
    with conn() as con:
        c = con.cursor()
        r = c.execute('select * from posters where status=1 order by id desc')
        posters = []
        for row in r:
            posters.append({
                'id': row[0],
                'code': row[1],
                'name': row[2],
                'preview': row[3],
                'json': row[4],
                'create_time': row[5],
                'update_time': row[6],
                # 'status': row[7],
            })
        return posters


def query_user_poster(poster_id: int):
    """查找用户所有海报"""
    with conn() as con:
        c = con.cursor()
        r = c.execute('select * from posters where id = ? limit 1', [poster_id])
        row = r.fetchone()
        # print(row)
        if row is not None:
            return {
                'id': row[0],
                'code': row[1],
                'name': row[2],
                'preview': row[3],
                'json': row[4],
                'create_time': row[5],
                'update_time': row[6],
                'status': row[7],
            }
        else:
            return None


def query_user_share(code: str):
    """查询分享记录"""
    with conn() as con:
        c = con.cursor()
        r = c.execute('select * from shares where code = ? limit 1', [code])
        row = r.fetchone()
        # print(row)
        if row is not None:
            return {
                'id': row[0],
                'code': row[1],
                'pid': row[2],
                'params': row[3],
                'create_time': row[4],
            }
        else:
            return None


def now_str(days=0):
    return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')


def save_user_poster(data, pd):
    """新增海报"""
    # print("新增海报")
    code = C.code(16)
    name = data['name']
    path = C.STORE_PREVIEW + code + "." + pd['type']
    im = poster.drawmini(pd)
    im.save(path)
    path = C.get_url_path(path)
    return db_save_poster(code, name, path, data['json'])


def update_user_poster(data, pd, id):
    """更新海报"""
    # print("更新海报: id=" + str(id))
    code = data.get('code', C.code(16))
    name = data['name']
    path = C.STORE_PREVIEW + code + "." + pd['type']
    im = poster.drawmini(pd)
    im.save(path)
    path = C.get_url_path(path)
    return db_update_poster(id, code, name, path, data['json'])


def save_or_update_user_poster(data):
    """保存海报"""
    # print(data)
    # 生成缩略图
    pd = json.loads(data['json'])
    print(pd)
    id = data.get('id', 0)
    if id == 0:
        # 新增海报
        return save_user_poster(data, pd)
    else:
        return update_user_poster(data, pd, id)


def copy_user_poster(id):
    """复制海报"""
    p = query_user_poster(id)
    if p:
        return db_save_poster(p['code'], p['name'] + '-复制', p['preview'], p['json'])
    return None


def get_share_link(param):
    """获取海报分享链接"""
    code = C.md5(param)
    url = f'/view/{code}.png'
    url = C.add_url_prefix(url)
    s = query_user_share(code)
    if s:
        return R.ok().add('url', url).json()
    # 需要保存链接
    poster_id = int(param['posterId'])
    p = query_user_poster(poster_id)
    if p is None:
        print('海报不存在')
        return R.error('海报不存在').json()
    # print('保存海报参数')
    db_save_share(code, poster_id, json.dumps(param))
    return R.ok().add('url', url).json()


def find_share_data(code):
    """查找分享记录"""
    s = query_user_share(code)
    if s is None:
        return None
    # print(s)
    params = json.loads(s['params'])

    poster_id = int(params['posterId'])
    p = query_user_poster(poster_id)

    data = json.loads(p['json'])
    items = data['items']
    dic = {}
    for item in items:
        vd = item['vd']
        if vd.strip():
            dic[vd] = item
    if p is None:
        return None
    for item in params.items():
        k = item[0]
        v = item[1]
        # 背景特殊处理
        if k == 'bgUrl':
            data['bgUrl'] = v
        if dic.get(k, None) is not None:
            dic[k]['v'] = v
    # print(json.dumps(data, indent=2))
    return data


def save_token(token):
    """保存token"""
    with conn() as con:
        c = con.cursor()
        params = [token, now_str(), now_str(days=10)]
        c.execute("insert into tokens (token, create_time, expire_time) values (?, ?, ?)", params)
        con.commit()
        return c.lastrowid


def query_token(token):
    """查询token"""
    with conn() as con:
        c = con.cursor()
        r = c.execute('select * from tokens where token = ? and expire_time >= ? limit 1', [token, now_str()])
        row = r.fetchone()
        print(row)
        return row is not None
    return None


if __name__ == '__main__':
    # db_save_poster('12', 'fdsf', 'dsfd', 'dsfd', '2010-12-23')
    print(now_str())
    print(now_str(days=10))
