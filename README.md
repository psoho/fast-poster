<p align="center"><a href="https://poster.prodapi.cn/doc/" target="_blank"><img width="100" src="https://poster.prodapi.cn/doc/assets/dragonfly.svg" alt="fast-poster logo"></a></p>

## 介绍

🔥🔥🔥 fastposter海报生成器是一款快速开发海报的工具，只需要上传一张海报底图，然后在对应的位置放上组件（`文字`、`图片`、`二维码`、`头像`），即可生成海报。用所见即所得的方式快速完成海报开发。

## 文档、在线示例

- 开发文档：[https://poster.prodapi.cn/doc/](https://poster.prodapi.cn/doc/)
- 在线体验：[https://poster.prodapi.cn/](https://poster.prodapi.cn/#from=2.8.3)
- 专业版：[https://poster.prodapi.cn/pro/](https://poster.prodapi.cn/pro/#from=2.8.3)

> 欢迎点亮小星星，加速项目开发

<a href="https://github.com/psoho/fast-poster" class="link github-link" target="_blank"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/psoho/fast-poster?style=social"></a>
<a href="https://gitee.com/psoho/fast-poster" class="link gitee-link" target="_blank"><img alt="gitee Repo stars" src="https://gitee.com/psoho/fast-poster/badge/star.svg"></a>

## 只需三步，即可完成海报开发

#### 一、启动服务

```bash
docker run -it --name fast-poster -p 5000:5000 tangweixin/fast-poster
```

#### 二、编辑海报

![fastposter编辑海报](https://poster.prodapi.cn/doc/assets/image-20220407142530149.png)


#### 三、生成代码

![fastposter生成代码](https://poster.prodapi.cn/doc/assets/image-20220407142705928.png)

请求示例

```bash
curl --location --request POST 'https://poster.prodapi.cn/api/link' \
--header 'Content-Type: application/json' \
--header 'token: ApfrIzxCoK1DwNZOEJCwlrnv6QZ0PCdv' \
--data-raw '{
  "f1": "名师定制",
  "f2": "8S服务体系",
  "f3": "高端资源",
  "f4": "名师定制",
  "title": "人工智能机器学习",
  "type": "高薪就业班",
  "id": 2
}'
```

响应示例

```json
{"code": 0, "msg": "success", "data": {"url": "https://poster.prodapi.cn/v/e670a0b84209a7d9"}}
```

### 适用场景：

- 电商主图编辑器
- 在线作图
- 电商海报编辑器
- Python Pillow绘图 Pillow制作海报
- Java生成二维码分享海报图片
- Java Graphics2D绘制海报图片
- 微信小程序生成海报分享朋友圈
- PHP生成二维码海报图片
- 自定义商业海报图片
- H5生成海报图片
- 二维码分享海报图片
- canvas生成海报图片
- 通过JSON生成海报图片


[comment]: <> "### 追星之路"

[comment]: <> "[![Stargazers over time]&#40;https://starchart.cc/psoho/fast-poster.svg&#41;]&#40;https://starchart.cc/psoho/fast-poster&#41;"

## 捐赠

如果你觉得 `fastposter` 对你有帮助，或者想对我们微小的工作一点支持，欢迎给我们[捐赠](https://poster.prodapi.cn/doc/guide/donate.html)

## 社区

进群加作者微信`fastposter`

![fastposer作者微信](https://poster.prodapi.cn/doc/assets/qrcode.jpeg)

## License


