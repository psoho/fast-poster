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
import poster
import store


class BaseHandler(RequestHandler):

    def set_default_headers(self) -> None:
        origin_url = self.request.headers.get('Origin')
        if not origin_url: origin_url = '*'
        self.set_header('Access-Control-Allow-Methods', 'POST, PUT, DELETE, GET, OPTIONS')
        self.set_header('fastposter', 'fastposter/v2.17.0')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Origin', origin_url)
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with,token,Content-type,Client-Type,Client-Version')

    def options(self):
        self.set_status(200)
        self.finish()

    def json(self, r: R):
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.write(r.json())


class BaseAuthHandler(BaseHandler):

    def prepare(self):
        self.check_token()

    def token(self):
        t = self.request.headers['token'] if 'token' in self.request.headers else None
        if not t:
            t = self.get_argument('token', None)
        if not t:
            t = self.get_body_argument('token', None)
        return t

    def check_token(self):
        t = self.token()
        if not t:
            self.json(R.expire('not token'))
            return self.finish()
        if not C.check_token(t):
            self.json(R.expire())
            return self.finish()


class ApiLoginHandler(BaseHandler):

    def post(self):
        token = self.get_body_argument('token')
        if C.check_token(token):
            self.json(R.ok('login success.').add('token', token))
        else:
            self.json(R.error('token not match!'))


class ApiPostersHandler(BaseAuthHandler):

    def get(self, id):
        poster = dao.query_user_poster(id)
        self.write(R.ok().add('poster', poster).json())


class ApiUserPostersHandler(BaseAuthHandler):

    def get(self):
        posters = dao.query_user_posters()
        self.write(R.ok().add('posters', posters).json())

    def delete(self, id):
        dao.db_delete_poster(int(id))
        self.write(R.ok().json())

    def post(self):
        data = json.loads(self.request.body)
        id = dao.save_or_update_user_poster(data)
        self.write(R.ok().add("id", id).json())


class ApiUserPostersCopyHandler(BaseAuthHandler):

    def post(self, id):
        id = dao.copy_user_poster(id)
        self.json(R.ok().add("id", id))


class ApiPreviewHandler(BaseAuthHandler):

    def post(self):
        data = json.loads(self.request.body)
        buf, mimetype = poster.drawio(data)
        self.set_header('Content-Type', mimetype)
        self.write(buf.getvalue())


class ApiUploadHandler(BaseAuthHandler):

    def post(self):
        for field_name, fs in self.request.files.items():
            for f in fs:
                filename, body, content_type = f["filename"], f['body'], f["content_type"]
                path = store.save(body, filename)
                break
        self.json(R.ok().add("url", path))


class ApiLinkHandler(BaseAuthHandler):

    def post(self):
        param = json.loads(self.request.body)
        code = C.md5(param, 16)
        if dao.get_share_link(code, param):
            url = f"{uri}/v/{code}".replace('//v', '/v')
            self.json(R.ok().add('url', url))
        else:
            self.json(R.error(f'the poster [{param["posterId"]}] not exits.'))


class ApiBuildPosterHandler(BaseAuthHandler):

    def post(self):
        args = json.loads(self.request.body)
        print(args)
        traceId = C.code(32)
        payload = args['payload']  # type: str
        if not payload.startswith("{"):
            # 需要base64解码
            payload = base64.b64decode(payload)
        data = dao.find_build_data(args['uuid'], json.loads(payload))
        if data is None:
            print('no poster here!')
            self.write(R.error('no poster here!'))
            return
        buf, mimetype = poster.drawio(data)
        self.set_header('fastposter-traceid', traceId)
        if args.get('b64', False):
            b64 = base64.b64encode(buf.read()).decode()
            self.write(b64)
        else:
            self.set_header('Content-Type', mimetype)
            self.write(buf.getvalue())


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


class MyStaticFileHandler(StaticFileHandler, BaseHandler):
    pass


def make_app(p):
    # path = "static" if C.indocker() else "../design/dist"
    path = "static"
    settings = {
        'debug': not C.indocker() or os.environ.get('POSTER_DEBUG', 'false') == 'true'
    }
    print('p', p)
    return Application([
        (f"{p}api/login", ApiLoginHandler),
        (f"{p}api/user/posters", ApiUserPostersHandler),
        (f"{p}api/user/posters/copy/(.+)", ApiUserPostersCopyHandler),
        (f"{p}api/user/posters/(.+)", ApiUserPostersHandler),
        (f"{p}api/user/poster/(.+)", ApiPostersHandler),
        (f"{p}api/preview", ApiPreviewHandler),
        (f"{p}api/upload", ApiUploadHandler),
        (f"{p}api/link", ApiLinkHandler),
        (f"{p}v1/build/poster", ApiBuildPosterHandler),
        (f"{p}v/(.+)", ApiViewHandler),
        (f'{p}(store/.*)$', StaticFileHandler, {"path": join(dirname(__file__), "data")}),
        (f'{p}resource/(.*)$', MyStaticFileHandler, {"path": join(dirname(__file__), "resource")}),
        (f'{p}(.*)$', StaticFileHandler, {"path": join(dirname(__file__), path), "default_filename": "index.html"})

    ], **settings)


if __name__ == "__main__":
    banner = '''
  __              _                       _               
 / _|            | |                     | |              
| |_   __ _  ___ | |_  _ __    ___   ___ | |_   ___  _ __ 
|  _| / _` |/ __|| __|| '_ \  / _ \ / __|| __| / _ \| '__|
| |  | (_| |\__ \| |_ | |_) || (_) |\__ \| |_ |  __/| |   
|_|   \__,_||___/ \__|| .__/  \___/ |___/ \__| \___||_|   
                      | |                                 
                      |_|                                 
                                    fastposter(v2.17.0)     
                             https://fastposter.net/doc/   
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
