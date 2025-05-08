<p align="center"><a href="https://fastposter.net/doc/" target="_blank"><img width="168" src="https://fastposter.net/dassets/dragonfly2x.png" alt="fast-poster logo"></a></p>

<p align="center">
  <a href="https://gitcode.com/psoho/fast-poster" class="link github-link" target="_blank"><img style="max-width: 100px;" alt="Gitcode Repo stars" src="https://gitcode.com/psoho/fast-poster/star/badge.svg"></a>
  <a href="https://github.com/psoho/fast-poster" class="link github-link" target="_blank"><img style="max-width: 100px;" alt="GitHub Repo stars" src="https://img.shields.io/github/stars/psoho/fast-poster?style=social"></a>
  <img alt="csharp" src="https://img.shields.io/badge/language-python-yellow.svg">
  <img alt="csharp" src="https://img.shields.io/badge/language-vue-brightgreen.svg">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img alt="version" src="https://img.shields.io/badge/version-2.19.1-brightgreen">
</p>

## Introduction

Fastposter is a rapid poster development tool that allows you to quickly create posters. Simply upload a background image and place components (`text`, `image`, `QR code`, `avatar`) in the desired positions to generate a poster. Click the `Code` button to directly generate SDK calling code in various languages, making development fast and easy.

It has served numerous e-commerce projects, with over `80,000` users across multiple projects. Tested in production environments over the years, it's proven to be stable and reliable. It is widely used in various e-commerce, distribution systems, e-commerce posters, e-commerce main images, and other poster generation and production scenarios.

> If this project has been helpful to you, please give it a star.

## Documentation

- Developer Documentation: [https://fastposter.net/doc/](https://fastposter.net/doc/)
- Java Professional Version - Online Experience: [https://fastposter.net/demo/java/](https://fastposter.net/demo/java/)
- Python Professional Version - Online Experience: [https://fastposter.net/demo/python/](https://fastposter.net/demo/python/)
- Community Version - Online Experience: [https://fastposter.net/demo/open/](https://fastposter.net/demo/open/)
- 🔥🔥Cloud Service - Free Trial: [https://fastposter.net/](https://fastposter.net/)

## Features

- Supports fast Docker deployment.
- Supports production-level e-commerce environments.
- Supports popular SDKs for quick development in `Java`, `Python`, `PHP`, `Go`, `JavaScript`, `mini-program`.
- No need to write complex rendering code.
- Supports multiple file formats: `jpeg`, `png`, `webp`, `pdf`, `base64`.
- Convenient code generation.


## Getting Started

### Step 1: Start the Service

```bash
docker run -it --name fastposter -p 5000:5000 fastposter/fastposter
```

### Step 2: Edit the Poster

![image-20230726174142177](https://fastposter.net/dassets/image-20230726174142177.png)


### Step 3: Generate Code

![image-20230726174208989](https://fastposter.net/dassets/image-20230726174208989.png)


Request Example (parameters can be passed directly):

```java
// 1. Create a poster client object
FastposterClient client = FastposterClient.builder()
        .endpoint("http://127.0.0.1:5000")      // Set the access endpoint
        .token("ApfrIzxCoK1DwNZOEJCwlrnv6QZ0PCdv")  // Set the token
        .build();

// 2. Prepare poster parameters
Map<String, Object> params = new HashMap<>();
params.put("name", "Test Text");

// 3. Generate and save the poster
client.buildPoster("80058c79d1e2e617").params(params).build().save("demo.png");
```

<img width=300 src="https://fastposter.net/dassets/demo.png" />

## Use Cases

- Poster generator
- Automatic poster generation tool
- Online poster design and generation
- Online poster maker
- Generate Moments (WeChat) posters
- E-commerce poster editor
- Certificate creation
- Automatic certificate generation tool
- QR code sharing poster images
- Create posters using Python Pillow
- E-commerce main image editor
- Generate QR code sharing posters using Java
- Create posters with Java Graphics2D
- Generate WeChat mini-program share posters
- Generate QR code posters using PHP
- Custom business poster images
- Generate HTML5 posters
- Create posters using HTML5 Canvas
- Generate posters using JSON data for batch production
- Draw images using BufferedImage

## Community

Author's WeChat: `fastposter`

![Author's WeChat](https://fastposter.net/dassets/qrcode.jpeg)




