import base64
import os
import re
from os.path import join, dirname

import tornado.ioloop
from tornado.web import RequestHandler, StaticFileHandler, Application

import C
import R
import dao
import json
import key
import poster
import store


class BaseHandler(RequestHandler):

    def set_default_headers(self) -> None:
        origin_url = self.request.headers.get('Origin')
        if not origin_url:
            origin_url = '*'
        self.set_header('Access-Control-Allow-Methods', 'POST, PUT, DELETE, GET, OPTIONS')
        self.set_header('Server', 'data')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Origin', origin_url)
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with,token,Content-type')

    def options(self):
        self.set_status(200)  # 这里的状态码一定要设置200
        self.finish()
        print('options')

    def check_token(self):
        # print('check_token', self.request.path)
        t = self.request.headers['token'] if 'token' in self.request.headers else None
        if not t:
            self.write(R.expire('not token').json())
            return self.finish()  # 标识请求已经结束
        dbtoken = dao.query_token(t)
        if not dbtoken:
            self.write(R.expire().json())
            return self.finish()

    def json(self, r: R):
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.write(r.json())


class ApiLoginHandler(BaseHandler):

    def post(self):
        accessKey = self.get_body_argument('accessKey')
        secretKey = self.get_body_argument('secretKey')
        print(f'login: accessKey={accessKey}, secretKey={secretKey}')
        if key.check(accessKey, secretKey):
            token = C.code(32)
            dao.save_token(token)
            # print('ok')
            self.write(R.ok('login success.').add('token', token).add('user', {'accessKey': accessKey,
                                                                               'secretKey': secretKey}).json())
        else:
            self.write(R.error('accessKey or secretKey not match!').json())


class ApiPostersHandler(BaseHandler):

    def prepare(self):
        self.check_token()  # 检查token是否有效
        ...

    def get(self, id):
        # 获取海报列表
        print(id)
        poster = dao.query_user_poster(id)
        self.write(R.ok().add('poster', poster).json())


class ApiUserPostersHandler(BaseHandler):

    def prepare(self):
        self.check_token()  # 检查token是否有效
        ...

    def get(self):
        # 获取海报列表
        posters = dao.query_user_posters()
        self.write(R.ok().add('posters', posters).json())

    def delete(self, id):
        # 删除指定的海报
        dao.db_delete_poster(int(id))
        self.write(R.ok().json())

    def post(self):
        data = json.loads(self.request.body)
        id = dao.save_or_update_user_poster(data)
        self.write(R.ok().add("id", id).json())


class ApiUserPostersCopyHandler(BaseHandler):

    def post(self, id):
        id = dao.copy_user_poster(id)
        self.write(R.ok().add("id", id).json())


class ApiPreviewHandler(BaseHandler):

    def post(self):
        data = json.loads(self.request.body)
        buf, mimetype = poster.drawio(data)
        self.set_header('Content-Type', mimetype)
        self.write(buf.getvalue())


class ApiUploadHandler(BaseHandler):

    def post(self):
        for field_name, fs in self.request.files.items():
            for f in fs:
                filename, body, content_type = f["filename"], f['body'], f["content_type"]
                path = store.save(body, filename)
                break
        self.write(R.ok().add("url", path).json())


class ApiLinkHandler(BaseHandler):

    def post(self):
        param = json.loads(self.request.body)
        # TODO: use http's Authorization header
        if not key.check(param['accessKey'], param['secretKey']):
            self.write(R.error('accessKey or secretKey not match').json())
        del param['accessKey']
        del param['secretKey']
        code = C.md5(param, 16)
        if dao.get_share_link(code, param):
            url = f"{uri}/v/{code}".replace('//v', '/v')
            self.json(R.ok().add('url', url))
        else:
            self.json(R.error(f'the poster [{param["posterId"]}] not exits.'))


class BaseDrawHandler(BaseHandler):

    async def async_drawio(self, data):
        return poster.drawio(data)

    def drawio(self, data):
        return poster.drawio(data)


class ApiViewHandler(BaseHandler):

    def get(self, code: str):
        c = code.split('.')
        data = dao.find_share_data(c[0])
        if data is None:
            print('no poster here!')
            self.write(R.error('no poster here!'))
            return
        if len(c) == 2 and (c[1] == 'png'):
            data['type'] = c[1]
        buf, mimetype = poster.drawio(data)
        if len(c) == 2 and c[1].startswith('b64'):
            b64 = base64.b64encode(buf.read()).decode()
            self.write(b64)
        else:
            self.set_header('Content-Type', mimetype)
            self.write(buf.getvalue())


class ApiB64Handler(BaseDrawHandler):

    def get(self, code):
        code = code[:code.index('.')]
        data = dao.find_share_data(code)
        if data is None:
            print('不好意思，海报不见了')
            return
        buf, mimetype = self.drawio(data)
        # self.set_header('Content-Type', mimetype)
        base64_data = base64.b64encode(buf.read())
        self.write(base64_data.decode())


class QrcodeHandler(BaseHandler):

    def get(self, v: str):
        data = {
            "w": 200,
            "h": 200,
            "bgc": "#ffffff",
            "type": "jpeg",
            "quality": 80,
            "bgUrl": "",
            "items": [
                {
                    "t": "qrcode",
                    "name": "二维码",
                    "uuid": "yI4GJ4a9",
                    "x": 10,
                    "y": 10,
                    "w": 180,
                    "h": 180,
                    "z": 1,
                    "s": 15,
                    "c": f"#010203",
                    "bgc": "#ffffff",
                    "v": f"{v}",
                    "vd": "qrcode",
                    "fn": "",
                    "st": 0,
                    "p": 0
                }
            ]
        }
        buf, mimetype = poster.drawio(data)
        self.set_header('Content-Type', mimetype)
        self.write(buf.getvalue())


class MyStaticFileHandler(StaticFileHandler, BaseHandler):
    pass


def make_app(p):
    path = "static" if C.indocker() else "../design/dist"
    settings = {
        'debug': not C.indocker() or os.environ.get('POSTER_DEBUG', 'false') == 'true'
    }
    return Application([
        (f"{p}api/login", ApiLoginHandler),
        (f"{p}api/user/posters", ApiUserPostersHandler),
        (f"{p}api/user/posters/copy/(.+)", ApiUserPostersCopyHandler),
        (f"{p}api/user/posters/(.+)", ApiUserPostersHandler),
        (f"{p}api/user/poster/(.+)", ApiPostersHandler),
        (f"{p}api/preview", ApiPreviewHandler),
        (f"{p}api/upload", ApiUploadHandler),
        (f"{p}api/link", ApiLinkHandler),
        (f"{p}api/qr/(.+)", QrcodeHandler),
        (f"{p}v/(.+)", ApiViewHandler),
        (f"{p}b64/(.+)", ApiB64Handler),
        (f'{p}(store/.*)$', StaticFileHandler, {"path": join(dirname(__file__), "data")}),
        (f'{p}resource/(.*)$', MyStaticFileHandler, {"path": join(dirname(__file__), "resource")}),
        (f'{p}(.*)$', StaticFileHandler, {"path": join(dirname(__file__), path), "default_filename": "index.html"})

    ], **settings)


if __name__ == "__main__":
    key.init()
    banner = '''
  __              _                       _               
 / _|            | |                     | |              
| |_   __ _  ___ | |_  _ __    ___   ___ | |_   ___  _ __ 
|  _| / _` |/ __|| __|| '_ \  / _ \ / __|| __| / _ \| '__|
| |  | (_| |\__ \| |_ | |_) || (_) |\__ \| |_ |  __/| |   
|_|   \__,_||___/ \__|| .__/  \___/ |___/ \__| \___||_|   
                      | |                                 
                      |_|                                 
                                    fastposter(v2.5.1)     
                             https://poster.prodapi.cn/docs/   
                                                            '''
    PORT = 5000
    print(banner)
    uri = os.environ.get('POSTER_URI_PREFIX', f'http://0.0.0.0:{PORT}/')
    print(f'Listening at {uri}\n')
    g = re.search(r'http[s]?://.*?(/.*)', uri)
    web_context_path = '/' if not g else g.group(1)
    app = make_app(web_context_path)
    app.listen(port=PORT, address='0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
