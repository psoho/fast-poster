<p align="center"><a href="https://poster.prodapi.cn/doc/" target="_blank"><img width="120" src="https://poster.prodapi.cn/doc/assets/dragonfly.svg" alt="fast-poster logo"></a></p>

<p align="center">
  <a href="https://github.com/psoho/fast-poster" class="link github-link" target="_blank"><img style="max-width: 100px;" alt="GitHub Repo stars" src="https://img.shields.io/github/stars/psoho/fast-poster?style=social"></a>
  <a href="https://gitee.com/psoho/fast-poster" class="link gitee-link" target="_blank"><img style="max-width: 100px;" alt="gitee Repo stars" src="https://gitee.com/psoho/fast-poster/badge/star.svg"></a>
  <img alt="csharp" src="https://img.shields.io/badge/language-python-yellow.svg">
  <img alt="csharp" src="https://img.shields.io/badge/language-vue-brightgreen.svg">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img alt="version" src="https://img.shields.io/badge/version-2.9.3-brightgreen">
</p>

## 介绍

🔥🔥🔥 fastposter海报生成器是一款快速开发海报的工具。只需上传一张背景图，在对应的位置放上组件（`文字`、`图片`、`二维码`、`头像`）即可生成海报。 点击`代码`直接生成各种语言的调用代码，方便快速开发。

现已服务众多电商类项⽬，多个项⽬有`52W+`⽤户，通过多年⽣产环境的考验，稳定可靠。广泛应用于各类电商、分销系统、电商海报、电商主图等海报生成和制作场景。

> 特别感谢大家的鼓励、捐赠和支持，开源不易、希望能够一直坚持。

## 文档

- 开发文档：[https://poster.prodapi.cn/doc/](https://poster.prodapi.cn/doc/)
- 在线体验：[https://poster.prodapi.cn/](https://poster.prodapi.cn/#from=2.9.3)
- 专业版-Python：[https://poster.prodapi.cn/pro/](https://poster.prodapi.cn/pro/#from=2.9.3)
- 专业版-Java：[https://poster.prodapi.cn/pro/java/](https://poster.prodapi.cn/pro/java/#from=2.9.3)

> 你点亮的小星星，正在加速项目开发迭代

## 特性

- 支持docker快速部署
- 支持电商级生产环境
- 支持多种编程语言 `Java` `Python` `PHP` `Golang` `JavaScript` `小程序`
- 无需编写复杂的绘图渲染代码
- 极低的服务器资源开销
- 支持多种文件格式 `jpeg` `png` `webp` `pdf` `base64`
- 便捷的代码生成
- 提供常用的组件 `文字` `头像` `图片` `二维码`


## 快速开始

### 一、启动服务

```bash
docker run -it --name fast-poster -p 5000:5000 tangweixin/fast-poster
```

### 二、编辑海报

![fastposter编辑海报](https://poster.prodapi.cn/doc/assets/image-20220407142530149.png)


### 三、生成代码

![fastposter生成代码](https://poster.prodapi.cn/doc/assets/image-20220407142705928.png)

请求示例（可直接传递需要的参数）

```bash
curl --location --request POST 'https://poster.prodapi.cn/api/link' \
--header 'Content-Type: application/json' \
--header 'token: ApfrIzxCoK1DwNZOEJCwlrnv6QZ0PCdv' \
--data-raw '{
  "title": "人工智能+机器学习",
  "id": 2
}'
```

响应示例（返回海报的访问地址）

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "url": "https://poster.prodapi.cn/v/90295c118d4c8802"
    }
}
```

## 适用场景

- 海报生成器
- 海报自动生成工具
- 海报在线设计生成器
- 海报生成器在线制作
- 生成朋友圈海报
- 电商海报编辑器
- 证书制作
- 证书自动生成工具
- 二维码分享海报图片
- Python Pillow绘图 Pillow制作海报
- 电商主图编辑器
- Java生成二维码分享海报图片
- Java Graphics2D绘制海报图片
- 微信小程序生成海报分享朋友圈
- PHP生成二维码海报图片
- 自定义商业海报图片
- H5生成海报图片
- canvas生成海报图片
- 通过JSON生成海报图片
- BufferdImage绘制图片

## 社区

作者微信`fastposter`

![fastposer作者微信](https://poster.prodapi.cn/doc/assets/qrcode.jpeg)
