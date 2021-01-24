<p align="center">
  <img src="./title.png" alt="FastAPI">
</p>

<p align="center">
    <em>
        FastAPI を使ってWEBアプリを作ってみる
    </em>
</p>

<p align="center">
    <img
        src="https://img.shields.io/badge/serialization-WIP-blue.svg?style=for-the-badge"
    />
    <a
        href="https://nmomos.com/tips/2021/01/24/fastapi-docker-3/"
        target="_blank"
    >
        <img
            src="https://img.shields.io/badge/newest-Part--3-orange.svg?style=for-the-badge"
        />
    </a>
</p>

# hedgehog-reservation

このリポジトリは 「FastAPI を使ってWEBアプリを作ってみる」 シリーズで作成したソースコードのサンプルです。
該当のページはココで発見できます:

**その1**: <a href="https://nmomos.com/tips/2021/01/23/fastapi-docker-1/" target="_blank">FastAPIとDockerでHelloWorld</a>

**その2**: <a href="https://nmomos.com/tips/2021/01/23/fastapi-docker-2/" target="_blank">AlembicとPostgreSQLでDB Migrate</a>

**その3**: <a href="https://nmomos.com/tips/2021/01/24/fastapi-docker-3/" target="_blank">APIエンドポイントをPostgreSQLに接続</a>

---

## サンプルコードの実行

リポジトリのクローン

```bash
$ git clone git@github.com:Nmomos/hedhehog-reservation.git
```

任意のパートにスイッチ

```bash
$ git switch part2

or

$ git checkout part2
```

イメージビルド

```bash
$ docker-compose build
```

コンテナの起動

```bash
$ docker-compose up -d
```

## API Documentへのアクセス

**Swagger:**
<a href="http://localhost:8000/docs" target="_blank">
    http://localhost:8000/docs
</a>

**Redoc:**
<a href="http://localhost:8000/docs" target="_blank">
    http://localhost:8000/redoc
</a>
