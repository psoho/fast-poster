import os
import traceback
from io import BytesIO

import qrcode
import requests
import requests_cache
import urllib3
from PIL import Image, ImageDraw, ImageFont

import C

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}

NO_IMG = Image.open(os.path.join(os.path.dirname(__file__), 'resource/img/no-img.jpg')).convert('RGBA')
requests_cache.install_cache(C.STORE_DB + '/cache')


def fetchImg(url=''):
    try:
        if url.startswith('store/upload/'):
            if os.path.exists(f'data/{url}'):
                return Image.open(f'data/{url}').convert('RGBA')
            else:
                return NO_IMG
        r = requests.get(url, timeout=0.2)
        return Image.open(BytesIO(r.content)).convert('RGBA')
    except urllib3.exceptions.ReadTimeoutError:
        return None
    except Exception:
        traceback.print_exc()
        return NO_IMG
    except urllib3.exceptions.ReadTimeoutError:
        print('xxx')
        return None


def drawImg(draw, d, bg):
    url, w, h, x, y = d['v'], d['w'], d['h'], d['x'], d['y']
    try:
        img = fetchImg(url)
        if img == None:
            return
        # 尺寸更改
        img = img.resize((w, h), Image.ANTIALIAS)
        bg.paste(img, (x, y), img)
    except Exception as e:
        print('绘制图片异常: %s' % e)
        pass


def drawBg(item):
    url = str(item['bgUrl'])
    w = item['w']
    h = item['h']
    c = item['bgc']
    c = '#fafbfc' if c == '' else c
    if not url.strip():
        img = Image.new('RGB', (w, h), c)
    else:
        img = fetchImg(url)
    img = img.resize((w, h), Image.ANTIALIAS)
    draw = ImageDraw.Draw(img)  # 绘制对象
    return img, draw


def getFont(item):
    fn = item['fn']
    size = item['s']
    if fn == "":
        fn = '0d44d315557a4a25.woff'
    font = 'resource/fonts/' + fn
    return ImageFont.truetype(font, size)


def wrap_text(text, font, width):
    """包裹文字"""
    sb = []
    temp = ''
    for s in text:
        t = temp + s
        if font.getsize(t)[0] > width:
            sb.append(temp)
            temp = s
        else:
            temp += s
    if temp != '':
        sb.append(temp)
    return sb


def drawText(draw, item, bg):
    font = getFont(item)
    v = item['v']
    w = item['w']
    h = item['h']
    x = item['x']
    y = item['y']
    c = item.get('c', '#010203')
    img = Image.new("RGBA", (w, h), '#fff0')
    draw = ImageDraw.Draw(img)  # type:ImageDraw.ImageDraw
    t = wrap_text(v, font, w)
    draw.text((0, 0), '\n'.join(t), fill=c, font=font)
    if img is not None:
        bg.paste(img, (x, y), img)


def drawQrCode(draw, item, bg):
    url = item['v']
    w = item['w']
    h = item['h']
    x = item['x']
    y = item['y']
    c = item.get('c', '#010203').strip()
    c = '#010203' if len(c) == 0 else c
    p = item.get('p', 0)
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=p,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=c, back_color="#ffffff")
    img = img.resize((w, h), Image.ANTIALIAS)
    bg.paste(img, (x, y), None)


def drawAvatar(draw, item, bg):
    url = item['v']
    w = item['w']
    h = item['h']
    x = item['x']
    y = item['y']
    c = item.get('c', '#ffffff').strip()
    c = '#ffffff' if len(c) == 0 else c
    im = fetchImg(url)
    if im == None:
        return
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)
    im = im.resize((w, h), Image.ANTIALIAS)
    mask = Image.new('RGBA', bigsize)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, outline=c, width=4 * 3)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.paste(mask, (0, 0), mask)
    bg.paste(im, (x, y), im)
    pass


def draw(data):
    img, draw = drawBg(data)

    for item in data['items']:
        type = item['t']
        if 'text' == type:
            drawText(draw, item, bg=img)
        if 'image' == type:
            drawImg(draw, item, bg=img)
        if 'avatar' == type:
            drawAvatar(draw, item, bg=img)
        if 'qrcode' == type:
            url = item.get('v', '')
            if url.startswith('img:'):
                url = url[4:]
                item['v'] = url
                drawImg(draw, item, bg=img)
            else:
                drawQrCode(draw, item, bg=img)

    if data['type'] == "jpeg":
        img = img.convert("RGB")
    return img


def drawio(data, scale=1):
    type = data['type']
    if type == "jpg":
        type = "jpeg"
        data['type'] = type
    mimetype = "image/" + data['type']
    img = draw(data)
    quality = data['quality']
    if scale < 1:
        w = img.size[0]
        h = img.size[1]
        img = img.resize((int(w * scale), int(h * scale)), Image.ANTIALIAS)
    buf = BytesIO()
    img.save(buf, type, quality=quality, progressive=True)
    buf.seek(0)
    return buf, mimetype
