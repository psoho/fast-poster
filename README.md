<p align="center"><a href="https://fastposter.net/doc/" target="_blank"><img width="168" src="https://fastposter.net/dassets/dragonfly2x.png" alt="fast-poster logo"></a></p>

<p align="center">
  <a href="https://github.com/psoho/fast-poster" class="link github-link" target="_blank"><img style="max-width: 100px;" alt="GitHub Repo stars" src="https://img.shields.io/github/stars/psoho/fast-poster?style=social"></a>
  <a href="https://gitee.com/psoho/fast-poster" class="link gitee-link" target="_blank"><img style="max-width: 100px;" alt="gitee Repo stars" src="https://gitee.com/psoho/fast-poster/badge/star.svg"></a>
  <img alt="csharp" src="https://img.shields.io/badge/language-python-yellow.svg">
  <img alt="csharp" src="https://img.shields.io/badge/language-vue-brightgreen.svg">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img alt="version" src="https://img.shields.io/badge/version-2.17.0-brightgreen">
</p>

## 介绍

fastposter海报生成器是一款快速开发海报的工具。只需上传一张背景图，在对应的位置放上组件（`文字`、`图片`、`二维码`、`头像`）即可生成海报。 点击`代码`直接生成各种语言SDK的调用代码，方便快速开发。

现已服务众多电商类项⽬，多个项⽬有`60W+`⽤户，通过多年⽣产环境的考验，稳定可靠。广泛应用于各类电商、分销系统、电商海报、电商主图等海报生成和制作场景。

> 如果项目有帮到您，请点亮你点亮的小星星

## 文档

- 开发文档：[https://fastposter.net/doc/](https://fastposter.net/doc/)
- Java专业版-在线体验：[https://fastposter.net/demo/java/](https://fastposter.net/demo/java/)
- Python专业版-在线体验：[https://fastposter.net/demo/python/](https://fastposter.net/demo/python/)
- 社区版-在线体验：[https://fastposter.net/demo/open/](https://fastposter.net/demo/open/)
- 🔥🔥云服务-免费试用：[https://fastposter.net/](https://fastposter.net/)

## 特性

- 支持docker快速部署
- 支持电商级生产环境
- 主流的SDK支持，方便快速开发 `Java` `Python` `PHP` `Go` `JavaScript` `小程序`
- 无需编写复杂的绘图渲染代码
- 支持多种文件格式 `jpeg` `png` `webp` `pdf` `base64`
- 便捷的代码生成


## 快速开始

### 一、启动服务

```bash
docker run -it --name fastposter -p 5000:5000 fastposter/fastposter
```

### 二、编辑海报

![image-20230726174142177](https://fastposter.net/dassets/image-20230726174142177.png)


### 三、生成代码

![image-20230726174208989](https://fastposter.net/dassets/image-20230726174208989.png)

请求示例（可直接传递需要的参数）

```java
// 1.创建海报客户端对象
FastposterClient client = FastposterClient.builder()
        .endpoint("http://127.0.0.1:5000")      // 设置接入端点
        .token("ApfrIzxCoK1DwNZOEJCwlrnv6QZ0PCdv")  // 设置token
        .build();

// 2.准备海报参数
Map<String, Object> params = new HashMap<>();
params.put("name", "测试文本");

// 3.生成海报并保存
client.buildPoster("80058c79d1e2e617").params(params).build().save("demo.png");
```

响应示例（返回海报图片二进制流）

<img width=300 src="https://fastposter.net/dassets/demo.png" />

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

![fastposer作者微信](https://fastposter.net/dassets/qrcode.jpeg)
