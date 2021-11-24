import datetime
import json
import sqlite3

import C
import poster
import R


def conn():
    return sqlite3.connect(C.STORE_DB + '/poster.sqlite')


def table(sql):
    name = sql.split(' ')[2].strip()
    # print(name)
    with conn() as con:
        c = con.cursor()
        r = c.execute("select count(1) from sqlite_master where tbl_name = ?", [name])
        if r.fetchone()[0] == 0:
            c.execute(sql)
            print(f"{name} created successfully.")


INIT_SQL = [
    'CREATE TABLE posters (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, code text, name text, preview text, json text, create_time date, update_time date, status integer)',
    'CREATE TABLE links (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, code text, pid integer, params text, create_time date)',
    'CREATE TABLE tokens (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, token text, create_time date, expire_time date)',
]


def init():
    C.init_path()
    for sql in INIT_SQL: table(sql)

init()


def db_save_poster(code: str, name: str, preview: str, json: str):
    with conn() as con:
        c = con.cursor()
        params = [code, name, preview, json, now_str(), int(C.STATUS_NORMAL)]
        c.execute("insert into posters (code, name, preview, json, create_time, status) values (?, ?, ?, ?, ?, ?)",
                  params)
        con.commit()
        return c.lastrowid


def db_update_poster(id: int, code: str, name: str, preview: str, json: str):
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
    with conn() as con:
        c = con.cursor()
        params = [code, poster_id, param, now_str()]
        c.execute("insert into links (code, pid, params, create_time) values (?, ?, ?, ?)", params)
        con.commit()
        return c.lastrowid


def query_user_posters():
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
    with conn() as con:
        c = con.cursor()
        r = c.execute('select * from links where code = ? limit 1', [code])
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
    code = C.code(16)
    name = data['name']
    path = C.STORE_PREVIEW + code + "." + pd['type']
    im = poster.drawmini(pd)
    im.save(path)
    path = C.get_url_path(path)
    return db_save_poster(code, name, path, data['json'])


def update_user_poster(data, pd, id):
    code = data.get('code', C.code(16))
    name = data['name']
    path = C.STORE_PREVIEW + code + "." + pd['type']
    im = poster.drawmini(pd)
    im.save(path)
    path = C.get_url_path(path)
    return db_update_poster(id, code, name, path, data['json'])


def save_or_update_user_poster(data):
    pd = json.loads(data['json'])
    print(pd)
    id = data.get('id', 0)
    if id == 0:
        return save_user_poster(data, pd)
    else:
        return update_user_poster(data, pd, id)


def copy_user_poster(id):
    p = query_user_poster(id)
    if p:
        return db_save_poster(p['code'], p['name'] + '-复制', p['preview'], p['json'])
    return None


def get_share_link(code, param):
    s = query_user_share(code)
    if s:
        return True
    posterId = int(param['posterId'])
    p = query_user_poster(posterId)
    if p is None:
        print('海报不存在')
        return R.error('海报不存在').json()
    db_save_share(code, posterId, json.dumps(param))
    return True


def find_share_data(code):
    s = query_user_share(code)
    if s is None:
        return None
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
        if k == 'bgUrl':
            data['bgUrl'] = v
        if dic.get(k, None) is not None:
            dic[k]['v'] = v
    return data


def save_token(token):
    with conn() as con:
        c = con.cursor()
        params = [token, now_str(), now_str(days=10)]
        c.execute("insert into tokens (token, create_time, expire_time) values (?, ?, ?)", params)
        con.commit()
        return c.lastrowid


def query_token(token):
    with conn() as con:
        c = con.cursor()
        r = c.execute('select * from tokens where token = ? and expire_time >= ? limit 1', [token, now_str()])
        row = r.fetchone()
        print(row)
        return row is not None
    return None
