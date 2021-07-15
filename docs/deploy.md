# 部署

## 公网部署

部署到公网环境，需要设置变量`POSTER_URI_PREFIX`，把`127.0.0.1`替换成`服务器的IP`即可

```bash
docker run -e POSTER_URI_PREFIX=http://127.0.0.1:9001/ --name fast-poster -p 9001:9001 tangweixin/fast-poster
```

`docker-compose.yml`方式

```yaml
version: '3'
services:
  fastposter:
    container_name: fastposter
    image: tangweixin/fast-poster
    ports:
      - 9001:9001
    environment:
      POSTER_URI_PREFIX: http://127.0.0.1:9001/
```

## 账号密码

自定义账号密码，需要设置变量`ACCESS_KEY` `SECRET_KEY`

```bash
docker run -e ACCESS_KEY=ApfrIzxCoK1DwNZO -e SECRET_KEY=EJCwlrnv6QZ0PCdvrWGi --name fast-poster -p 9001:9001 tangweixin/fast-poster 
```

`docker-compose.yml`方式

```yaml
version: '3'
services:

  fastposter:
    container_name: fastposter
    image: tangweixin/fast-poster
    restart: on-failure
    ports:
      - 9001:9001
    environment:
      ACCESS_KEY: ApfrIzxCoK1DwNZO
      SECRET_KEY: EJCwlrnv6QZ0PCdvrWGi
```

## 数据持久化

持久化数据和图片资源，需要挂载目录`-v $PWD/fastposter/db:/app/db` `-v $PWD/fastposter/storage:/app/static/storage`

```bash
docker run -v $PWD/fastposter/db:/app/db -v $PWD/fastposter/storage:/app/static/storage --name fast-poster -p 9001:9001 tangweixin/fast-poster
```

`docker-compose.yml`方式

```yaml
version: '3'
services:

  fastposter:
    container_name: fastposter
    image: tangweixin/fast-poster
    ports:
      - 9001:9001
    volumes:
      - ./fastposter/db:/app/db
      - ./fastposter/storage:/app/static/storage

```

## 完整配置

```yaml
version: '3'
services:

  fastposter:
    container_name: fastposter
    image: tangweixin/fast-poster
    restart: on-failure
    ports:
      - 9001:9001
    volumes:
      - ./fastposter/db:/app/db
      - ./fastposter/storage:/app/static/storage
    environment:
      TZ: Asia/Shanghai
      ACCESS_KEY: ApfrIzxCoK1DwNZO
      SECRET_KEY: EJCwlrnv6QZ0PCdvrWGi
      POSTER_URI_PREFIX: http://127.0.0.1:9001/
```