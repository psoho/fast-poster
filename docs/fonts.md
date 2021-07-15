# 字体

## 版权

字体使用的是`阿里巴巴普惠体`中文字体，官方下载链接: [https://alibabafont.taobao.com/](https://alibabafont.taobao.com/)，大家遵守商业版权规范使用，切勿用于`违法用途`。

下载完成后，获得以下字体文件
```bash 
.
├── Alibaba-PuHuiTi-Bold.ttf
├── Alibaba-PuHuiTi-Heavy.ttf
├── Alibaba-PuHuiTi-Light.ttf
├── Alibaba-PuHuiTi-Medium.ttf
└── Alibaba-PuHuiTi-Regular.ttf
```

## 更换字体

把自己的字体放到项目的`fonts`目录即可，并更改`poster.py`相关字体代码即可。

```python
def getFont(item):
    """获取字体"""
    fn = item['fn']
    size = item['s']
    if fn == "":
        # fn = 'Alibaba-Emoji.ttf'
        # 更换相关字体
        # fn = 'Alibaba-PuHuiTi-Light.ttf'
        fn = 'Alibaba-PuHuiTi-Regular.otf'
    font = 'fonts/' + fn
    return ImageFont.truetype(font, size)
```





