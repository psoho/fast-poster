<p align="center"><a href="https://poster.prodapi.cn/doc/" target="_blank"><img width="120" src="https://poster.prodapi.cn/doc/assets/dragonfly.svg" alt="fast-poster logo"></a></p>

<p align="center">
<a href="https://github.com/psoho/fast-poster" class="link github-link" target="_blank"><img style="max-width: 100px;" alt="GitHub Repo stars" src="https://img.shields.io/github/stars/psoho/fast-poster? style=social"></a>
<a href="https://gitee.com/psoho/fast-poster" class="link gitee-link" target="_blank"><img style="max-width: 100px;" alt="gitee Repo stars" src="https://gitee.com/psoho/fast-poster/badge/star.svg"></a>
<img alt="csharp" src="https://img.shields.io/badge/language-python-yellow.svg">
<img alt="csharp" src="https://img.shields.io/badge/language-vue-brightgreen.svg">
<img alt="license" src="https://img.shields.io/badge/license-MIT-blue.svg">
<img Alt = "version" SRC = "https://img.shields.io/badge/version-2.11.0-brightgreen" >
</p>

## Introduction

🔥🔥🔥 fastposter Generator is a quick poster development tool. Just upload a background image, put the components (' text ', 'picture', 'QR code', 'avatar') in the corresponding position to generate a poster. Click 'code' to directly generate a variety of language call code, convenient for rapid development.

Now it has served a large number of e-commerce projects, many of which have '52W+' users. It has passed the test of production environment for many years and is stable and reliable. Widely used in all kinds of e-commerce, distribution systems, e-commerce posters, e-commerce main picture and other poster generation and production scenes.

> Thank you very much for your encouragement, donation and support. Open source is not easy, I hope I can stick to it.

## Document

- development documentation: [https://poster.prodapi.cn/doc/](https://poster.prodapi.cn/doc/)
- online experience: [https://poster.prodapi.cn/](https://poster.prodapi.cn/#from=2.11.0)
- ProPython: [https://poster.prodapi.cn/pro/](https://poster.prodapi.cn/pro/#from=2.11.0)
- ProJava: [https://poster.prodapi.cn/pro/java/](https://poster.prodapi.cn/pro/java/#from=2.11.0)

> The little star you lit is accelerating the project development iteration

## Features

- Supports docker rapid deployment
- Support e-commerce production environment
- Support for multiple programming languages' Java ', 'Python', 'PHP', 'Golang', 'JavaScript', 'mini programs'
- No need to write complex drawing rendering code
- Very low server resource overhead
- Support for multiple file formats: jpeg, png, webp, pdf, base64
- Easy code generation
- Provide common components' text ' 'avatar' 'picture' 'two-dimensional code'


## Quick Start

1. Start the service

```bash
docker run -it --name fast-poster -p 5000:5000 tangweixin/fast-poster
```

2. Edit the poster

![fastposter edit posters](https://poster.prodapi.cn/doc/assets/image-20220407142530149.png?v=2.11.0)


3. Generate code

![fastposter generated code](https://poster.prodapi.cn/doc/assets/image-20220407142705928.png?v=2.11.0)

Sample request (you can pass the required parameters directly)

```bash
curl --location --request POST 'https://poster.prodapi.cn/api/link' \
--header 'Content-Type: application/json' \
--header 'token: ApfrIzxCoK1DwNZOEJCwlrnv6QZ0PCdv' \
--data-raw '{
"title": Artificial Intelligence + Machine learning,
"id": 2
} '
```

Sample response (Return the poster's access address)

```json
{
  "code": 0,
  "msg": "success",
    "data": {
      "url": "https://poster.prodapi.cn/v/90295c118d4c8802"
    }
}
```

## Application scenario

- Poster Generator
- Automatic poster generation tool
- Poster online design generator
- Poster generator made online
- Generate a circle of Friends poster
- E-commerce poster editor
- Certificate Making
- Automatic certificate generation tool
- QR code to share poster pictures
- Python Pillow drawing Pillow makes posters
- E-commerce main chart editor
- Java generates QR code to share poster pictures
- Java Graphics2D draws the poster picture
- wechat mini program to generate posters to share moments
- PHP generates a two-dimensional code poster image
- Custom commercial poster images
-H5 Generates poster images
- canvas Generates poster images
- Generate poster images via JSON
- BufferdImage Draws pictures

## Community

The author of wechat 'fastposter'

![fastposer author WeChat](https://poster.prodapi.cn/doc/assets/qrcode.jpeg)