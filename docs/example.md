# 代码示例


## Python

依赖`requests`

```python
import requests
import json

class posterapi():

    def __init__(self, endpoint: str, accessKey: str, secretKey: str):
        if endpoint.endswith("/"):
            endpoint = endpoint[0:-1]
        self.endpoint = endpoint
        self.accessKey = accessKey
        self.secretKey = secretKey

    def getUrl(self, posterId: str, params: dict = {}):
        params = dict(params)
        params['posterId'] = posterId
        params['accessKey'] = self.accessKey
        params['secretKey'] = self.secretKey
        url = f"{self.endpoint}/api/link"
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps(params)
        response = requests.request("POST", url, headers=headers, data=payload)
        link = response.json()['url']  # type:str
        if not link.startswith('http'):
            link = self.endpoint + link
        self.link = link
        return link

    def save(self, filename='tmp.jpg'):
        response = requests.request("GET", self.link)
        with open(filename, mode='wb') as f:
            f.write(response.content)

if __name__ == '__main__':
    api = posterapi('http://localhost:9001/', 'ApfrIzxCoK1DwNZO', 'EJCwlrnv6QZ0PCdvrWGi')
    params = {}
    params["mainUrl"]="http://127.0.0.1:9001/storage/upload/bc7fd728cf40ef1c.jpg"
    params["payPrice"]="388"
    params["qrcode"]="https://poster.prodapi.cn/#from=qrcode"
    params["discountPrice"]="9.9"
    params["desc"]="泸州老窖 特曲 52度 浓香型白酒 500ml （百年品牌 泸州老窖荣誉出品）（新老包装随机发货）"
    params["realPrice"]="388"

    url = api.getUrl('2', params)
    print(url)
    api.save()
```

## Java

依赖`okhttp3`、`fastjson`、`commons-io`，请在`pom.xml`文件中，添加以下依赖

```xml
<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp</artifactId>
    <version>3.14.1</version>
</dependency>

<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>1.2.57</version>
</dependency>

<dependency>
    <groupId>commons-io</groupId>
    <artifactId>commons-io</artifactId>
    <version>2.6</version>
</dependency>
```

```java
import java.util.HashMap;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import okhttp3.*;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class FastPosterClientDemo {

    public static void main(String[] args) {

        // 创建海报客户端对象
        FastPosterClient posterClient = new FastPosterClient("http://localhost:9001/", "ApfrIzxCoK1DwNZO", "EJCwlrnv6QZ0PCdvrWGi");

        // 构造海报参数
        HashMap<String, String> params = new HashMap<>();
        params.put("mainUrl", "http://127.0.0.1:9001/storage/upload/bc7fd728cf40ef1c.jpg");
        params.put("payPrice", "388");
        params.put("qrcode", "https://poster.prodapi.cn/#from=qrcode");
        params.put("discountPrice", "9.9");
        params.put("desc", "泸州老窖 特曲 52度 浓香型白酒 500ml （百年品牌 泸州老窖荣誉出品）（新老包装随机发货）");
        params.put("realPrice", "388");

        // 海报ID
        String posterId = "2";

        // 获取下载地址
        String url = posterClient.getUrl(posterId, params);
        System.out.println("url=" + url);

        // 保存到本地
        posterClient.saveToPath(url, "temp.png");

    }

}


class FastPosterClient {

    final static OkHttpClient okHttpClient = new OkHttpClient.Builder().connectTimeout(6, TimeUnit.SECONDS).build();
    private static final String USER_AGENT = "fast-poster-client-java";

    /**
     * 接入点
     */
    private String endpoint;
    /**
     * 访问KEY
     */
    private String accessKey;
    /**
     * 访问密码
     */
    private String secretKey;

    public FastPosterClient(String endpoint, String accessKey, String secretKey) {

        this.accessKey = accessKey;
        this.secretKey = secretKey;

        endpoint = endpoint.trim();
        if (endpoint.endsWith("/")) {
            endpoint = endpoint.substring(0, endpoint.length() - 1);
        }
        this.endpoint = endpoint;

    }

    /**
     * 获取海报访问地址
     *
     * @param posterId 海报ID
     * @param params   参数列表
     * @return String
     */
    public String getUrl(String posterId, Map<String, String> params) {
        if (params == null) {
            params = new HashMap<>();
        }
        params.put("accessKey", this.accessKey);
        params.put("secretKey", this.secretKey);
        params.put("posterId", posterId);

        String url = this.endpoint + "/api/link";

        MediaType mediaType = MediaType.parse("application/json");
        String json = JSON.toJSONString(params, true);
        RequestBody body = RequestBody.create(mediaType, json);
        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .addHeader("User-Agent", USER_AGENT)
                .addHeader("Content-Type", "application/json")
                .addHeader("cache-control", "no-cache")
                .build();

        try {
            Response response = okHttpClient.newCall(request).execute();
            String jsonR = response.body().string();
            JSONObject o = JSONObject.parseObject(jsonR);
            if (o.getInteger("code") == 0) {
                url = o.getString("url");
            } else {
                throw new RuntimeException("获取海报链接异常: " + o.getString("msg"));
            }

            return url.startsWith("http") ? url : endpoint + "/" + url;
        } catch (IOException e) {
            throw new RuntimeException("获取海报链接异常", e);
        }
    }

    /**
     * 获取海报数据
     *
     * @param url
     * @return
     */
    public byte[] getData(String url) {
        try {
            Request request = new Request.Builder()
                    .url(url)
                    .addHeader("User-Agent", USER_AGENT)
                    .get()
                    .build();
            Response response = okHttpClient.newCall(request).execute();
            return response.body().bytes();
        } catch (Exception e) {
            throw new RuntimeException("获取海报数据异常", e);
        }
    }

    /**
     * 保存海报到文件
     *
     * @param url
     * @param path
     */
    public void saveToPath(String url, String path) {
        try {
            byte[] data = getData(url);
            FileUtils.writeByteArrayToFile(new File(path), data);
        } catch (IOException e) {
            new RuntimeException("保存海报到文件", e);
        }
    }

}

```

## PHP

```php
<?php

# 设置参数
$data = '{
  "mainUrl": "http://127.0.0.1:9001/storage/upload/bc7fd728cf40ef1c.jpg",
  "payPrice": "388",
  "qrcode": "https://poster.prodapi.cn/#from=qrcode",
  "discountPrice": "9.9",
  "desc": "泸州老窖 特曲 52度 浓香型白酒 500ml （百年品牌 泸州老窖荣誉出品）（新老包装随机发货）",
  "realPrice": "388",
  "accessKey": "ApfrIzxCoK1DwNZO",
  "secretKey": "EJCwlrnv6QZ0PCdvrWGi",
  "posterId": 2
}';

function get_link($data)
{
    $curl = curl_init();
    curl_setopt_array($curl, array(
        CURLOPT_URL => 'http://localhost:9001/api/link',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => '',
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 0,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => 'POST',
        CURLOPT_HTTPHEADER => array('Content-Type: application/json'),
        CURLOPT_POSTFIELDS => $data,
    ));
    $json = curl_exec($curl);
    curl_close($curl);
    $r = json_decode($json, true);
    return "http://localhost:9001/" . $r["url"];;
}

# 获取连接
$url = get_link($data);
echo "链接地址为: " . $url . "\n";

function down($url, $filename)
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $st = curl_exec($ch);   //将curl的结果存到变量里
    $fd = fopen($filename, 'w');
    fwrite($fd, $st);  //将curl的结果写入文件里
    fclose($fd);
    curl_close($ch);
}

# 下载并且, 保存图片
down($url, "temp.png");
echo "图片保存完成\n";

```

## Golang

```go

package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

func main() {

	url := "http://localhost:9001/api/link"
	method := "POST"

	payload := strings.NewReader(`{
    "mainUrl": "http://127.0.0.1:9001/storage/upload/bc7fd728cf40ef1c.jpg",
    "payPrice": "388",
    "qrcode": "https://poster.prodapi.cn/#from=qrcode",
    "discountPrice": "9.9",
    "desc": "泸州老窖 特曲 52度 浓香型白酒 500ml （百年品牌 泸州老窖荣誉出品）（新老包装随机发货）",
    "realPrice": "388",
    "accessKey": "ApfrIzxCoK1DwNZO",
    "secretKey": "EJCwlrnv6QZ0PCdvrWGi",
    "posterId": 2
}`)

	client := &http.Client {
	}
	req, err := http.NewRequest(method, url, payload)

	if err != nil {
		fmt.Println(err)
		return
	}
	req.Header.Add("Content-Type", "application/json")

	res, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer res.Body.Close()

	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(string(body))
}
```

## 验证

可以将生成的代码，直接放到`在线环境`中运行检验。以下是一些在线环境地址。

- [https://www.dooccn.com/](https://www.dooccn.com/)
