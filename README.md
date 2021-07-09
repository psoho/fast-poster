## fastposter海报生成器

### 介绍

**fastposter海报生成器，一分钟完成海报开发。**

- 在线体验：[https://poster.prodapi.cn/](https://poster.prodapi.cn/#from=v1.4.2)
- 只要一个 [Github Star](https://github.com/psoho/fast-poster) 就可以鼓励作者尽快完成 `剩下的 15%`
- 只要一个 [Gitee Star](https://gitee.com/psoho/fast-poster) 就可以鼓励作者尽快完成 `剩下的 15%`

### 特性

- 快速：三步完成海报开发工作
- 易用：无需名师指导，组件丰富、支持拖拽、复制、所见即所得、下载等功能
- 强大：不惧怕设计师更改海报设计，无需更改代码，从容应对UI变更
- 高效：只需拖拽组件就能生成海报的调用代码，极大降低开发人员的工作量

### 三步完成海报开发工作

#### 一、启动服务

1. 通过docker启动:
```bash
docker run --name fast-poster -p 9001:9001 tangweixin/fast-poster
```

2. 通过代码启动: 

```bash
# 安装依赖 
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 启动应用（需要在当前代码目录运行）
python app.py -k ApfrIzxCoK1DwNZO -s EJCwlrnv6QZ0PCdvrWGi
```

3.  打开浏览器: [http://127.0.0.1:9001/](http://127.0.0.1:9001/)

#### 二、编辑海报

点击`新建`按钮，在`海报设置` > `背景图⽚` ，点击`上传`⼀个海报背景图。

点击所需的控件【⽂本、⼆维码、头像、图⽚】，拖动调整位置，设置相关参数。

点击`预览`，可以实时查看最终⽣成的效果。

![输入图片说明](https://fastposter.oss-cn-shanghai.aliyuncs.com/v1.4.0/WX20210707-232649%402x.png)

#### 三、生成代码：

保存海报，然后点击`代码`，可以查看相关的语言调⽤代码。

![输入图片说明](https://fastposter.oss-cn-shanghai.aliyuncs.com/v1.4.0/WX20210707-232717%402x.png)


### 参与贡献

* [Alex-独孤求胜](https://gitee.com/sunlightcs)
* [nico1988](https://gitee.com/nico1988)
* [tangweixin](https://gitee.com/tangweixin)

### 赞赏

如果`fastposter`给您带了方便，不妨支持一下我们这个小团队。

![输入图片说明](https://fastposter.oss-cn-shanghai.aliyuncs.com/v1.4.0/%E6%8D%90%E8%B5%A0.jpg)

### 项目背景

在以前，通过程序绘制海报，需要熟悉各种语言底层（枯涩难懂）的绘图API，如`Java`需要熟悉`Graphics2D`。 接下来就是各种元素位置的调整，这是相当费眼睛的开发。

于是，一个通用的海报生成器应运而生，让开发人员无需关心底层的绘图API，用所见即所得的方式来完成开发。有更多的时间陪伴家人和朋友。

经过N次迭代和线上生产环境的考验。

`fastposter`海报生成器，是经过众多电商项⽬后，由于经常遇到需要⽣成海报的需求，所以特别开发的⼀款⼯具。

期间也参考了很多类似项⽬，最开始⽤ `Java` 实现。后⾯发现海报效果不是特别理想，达不到像素级要求。最后使⽤ `Python` 全⾯重构，效果⽐较满意。

现在已经服务了好⼏个电商项⽬，多个项⽬有`33.8W+`⽤户，通过过⽣产的考验，稳定可靠。

如果⼤家在使⽤过程中，发现有任何问题，欢迎添加 微信 进⾏反馈。

### 授权说明

从v1.4.0版本开始，为了项目和团队的健康发展，我们修改开源授权许可协议为GPL3.0，请商业使用的小伙伴注意。如果需要更宽松的授权，请扫码联系我们。

### 软件架构

技术栈
* `Java`
* `Python`
* `Tornado`
* `Vue`
* `Vuex`

客户端调用支持`Java` `Python` `PHP` `cURL` `JS` 等可以发送`HTTP`请求的语言.

### 性能测试

```bash
wrk -d 6s http://127.0.0.1:9001/view/5b0b06feeb582fdce2973a4ae227b2f0.png
```