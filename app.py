import base64
import os

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
        # self.set_header('Access-Control-Allow-Methods', 'POST, PUT, DELETE, GET, OPTIONS')
        self.set_header('Server', 'fastposter')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Origin', origin_url)
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with,token,Content-type')

    def options(self):
        self.set_status(200)  # 这里的状态码一定要设置200
        self.finish()
        print('options')

    def check_token(self):
        print('check_token', self.request.path)
        t = self.request.headers['token'] if 'token' in self.request.headers else None
        if not t:
            self.write(R.expire('not token').json())
            return self.finish()  # 标识请求已经结束
        dbtoken = dao.query_token(t)
        if not dbtoken:
            self.write(R.expire().json())
            return self.finish()


class ApiLoginHandler(BaseHandler):

    def post(self):
        accessKey = self.get_body_argument('accessKey')
        secretKey = self.get_body_argument('secretKey')
        print(f'accessKey={accessKey}, secretKey={secretKey}')
        if key.check(accessKey, secretKey):
            token = C.code(32)
            dao.save_token(token)
            print('ok')
            self.write(
                R.ok('login success.').add('token', token).add('user',
                                                               {'accessKey': accessKey, 'secretKey': secretKey}).json())
        else:
            self.write(R.error('accessKey or secretKey not match!').json())


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
        items = store.uploads(self.request.files)
        path = items[0]
        self.write(R.ok().add("url", path).json())


class ApiLinkHandler(BaseHandler):

    def post(self):
        param = json.loads(self.request.body)
        if not key.check(param['accessKey'], param['secretKey']):
            self.write(R.error('accessKey or secretKey not match').json())
        self.write(dao.get_share_link(param))


class BaseDrawHandler(BaseHandler):

    async def async_drawio(self, data):
        return poster.drawio(data)

    def drawio(self, data):
        return poster.drawio(data)


class ApiViewHandler(BaseDrawHandler):

    async def get(self, code):
        code = code[:code.index('.')]
        data = dao.find_share_data(code)
        if data is None:
            print('不好意思，海报不见了')
            return
        buf, mimetype = await self.async_drawio(data)
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


def make_app():
    settings = {
        'debug': True
    }
    return Application([
        (r"/api/login", ApiLoginHandler),
        (r"/api/user/posters", ApiUserPostersHandler),
        (r"/api/user/posters/copy/(.+)", ApiUserPostersCopyHandler),
        (r"/api/user/posters/(.+)", ApiUserPostersHandler),
        (r"/api/preview", ApiPreviewHandler),
        (r"/api/upload", ApiUploadHandler),
        (r"/api/link", ApiLinkHandler),
        (r"/view/(.+)", ApiViewHandler),
        (r"/b64/(.+)", ApiB64Handler),
        ## 静态化文件特殊处理
        (r'^/(.*)$', StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static"), "default_filename": "index.html"}),

    ], **settings)


if __name__ == "__main__":
    key.init()  # key 初始化
    banner = '''  __              _                       _               
     / _|            | |                     | |              
    | |_   __ _  ___ | |_  _ __    ___   ___ | |_   ___  _ __ 
    |  _| / _` |/ __|| __|| '_ \  / _ \ / __|| __| / _ \| '__|
    | |  | (_| |\__ \| |_ | |_) || (_) |\__ \| |_ |  __/| |   
    |_|   \__,_||___/ \__|| .__/  \___/ |___/ \__| \___||_|   
                          | |                                 
                          |_|                                 
                                        fastposter(v1.5.3)     '''
    app = make_app()
    print(banner)
    app.listen(port=9001, address='0.0.0.0')
    print(f'http://0.0.0.0:9001/')
    tornado.ioloop.IOLoop.current().start()
