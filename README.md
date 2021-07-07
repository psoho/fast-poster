## fast-poster通用海报生成器

### 介绍

一个快速开发动态海报的工具

- 在线体验：[https://poster.prodapi.cn/](https://poster.prodapi.cn/#from=v1.4.1)
- 只要一个 [Github Star](https://github.com/psoho/fast-poster) 就可以鼓励作者尽快完成 `剩下的 15%`
- 只要一个 [Gitee Star](https://gitee.com/psoho/fast-poster) 就可以鼓励作者尽快完成 `剩下的 15%`

### 演示

![输入图片说明](https://fastposter.oss-cn-shanghai.aliyuncs.com/v1.4.0/WX20210706-004423%402x.png "WX20210615-081039.jpg")

### 特性

- 快速：三步完成海报开发工作：`启动服务` > `编辑海报` > `生成代码`
- 易用：组件丰富、支持拖拽、复制、所见即所得、下载等功能。
- 方便：无需更改代码，直接在编辑器修改海报即可获得最新的海报。

#### 一、启动服务

1. 运行命令: 
```bash
docker run --name fast-poster -p 9001:9001 tangweixin/fast-poster
```

2.  打开浏览器: [http://127.0.0.1:9001/](http://127.0.0.1:9001/)

#### 二、编辑海报

点击`新建`按钮，在`海报设置` > `背景图⽚` ，点击`上传`⼀个海报背景图。

点击所需的控件【⽂本、⼆维码、头像、图⽚】，拖动调整位置，设置相关参数。

点击`预览`，可以实时查看最终⽣成的效果。

![输入图片说明](https://fastposter.oss-cn-shanghai.aliyuncs.com/v1.4.0/WX20210706-004414%402x.png "WX20210615-081414.jpg")

#### 三、生成代码：

保存海报，然后点击`代码`，可以查看相关的语言调⽤代码。

![输入图片说明](https://fastposter.oss-cn-shanghai.aliyuncs.com/v1.4.0/WX20210706-004444%402x.png "WX20210615-081414.jpg")


### 参与贡献

* [Alex-独孤求胜](https://gitee.com/sunlightcs)
* [nico1988](https://gitee.com/nico1988)
* [tangweixin](https://gitee.com/tangweixin)

### 赞赏

如果`fastposter`给您带了方便，不妨支持一下我们这个小团队。

![输入图片说明](https://images.gitee.com/uploads/images/2021/0609/152314_a6c2dbc5_301987.jpeg "微信.jpg")

### 项目背景

在以前，通过程序绘制海报，需要熟悉各种语言底层（枯涩难懂）的绘图API，如`Java`需要熟悉`Graphics2D`。
接下来就是各种元素位置的调整，这是相当费眼睛的开发。

于是，一个通用的海报生成器应运而生，让开发人员无需关心底层的绘图API，用所见即所得的方式来完成开发。有更多的时间陪伴家人和朋友。

经过N次迭代和线上生产环境的考验。


`fast-poster`海报生成器，是经过众多电商项⽬后，由于经常遇到需要⽣成海报的需求，所以特别开发的⼀款⼯具。

期间也参考了很多类似项⽬，最开始⽤ `Java` 实现。后⾯发现海报效果不是特别理想，达不到像素级要求。最后使⽤ `Python` 全⾯重构，效果⽐较满意。

现在已经服务了好⼏个电商项⽬，多个项⽬有`33W+`⽤户，通过过⽣产的考验，稳定可靠。

如果⼤家在使⽤过程中，发现有任何问题，欢迎添加 微信 进⾏反馈。


### 授权说明

从v1.4.1版本开始，为了项目和团队的健康发展，我们修改开源授权许可协议为GPL3.0，请商业使用的小伙伴注意。如果需要更宽松的授权，请扫码联系我们。

### 软件架构

技术栈
* `Java`
* `Python`
* `Tornado`
* `Vue`
* `Vuex`

客户端调用支持`Java` `Python` `PHP` `cURL` `JS` 等可以发送`HTTP`请求的语言.



