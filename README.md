<p align="center">
  <img src=".github/title.png" alt="FastAPI">
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
        href="https://nmomos.com/tips/2021/02/21/fastapi-docker-7/"
        target="_blank"
    >
        <img
            src="https://img.shields.io/badge/newest-Part--7-orange.svg?style=for-the-badge"
        />
    </a>
</p>

# hedgehog-reservation

このリポジトリは 「FastAPI を使って WEB アプリを作ってみる」 シリーズで作成したソースコードのサンプルです。
該当のページはココで発見できます:

**その 1**: <a href="https://nmomos.com/tips/2021/01/23/fastapi-docker-1/" target="_blank">FastAPI と Docker で HelloWorld</a>

**その 2**: <a href="https://nmomos.com/tips/2021/01/23/fastapi-docker-2/" target="_blank">Alembic と PostgreSQL で DB Migrate</a>

**その 3**: <a href="https://nmomos.com/tips/2021/01/24/fastapi-docker-3/" target="_blank">API エンドポイントを PostgreSQL に接続</a>

**その 4**: <a href="https://nmomos.com/tips/2021/01/25/fastapi-docker-4/" target="_blank">Pytest と Docker でテスト構築</a>

**その 5**: <a href="https://nmomos.com/tips/2021/02/06/fastapi-docker-5/" target="_blank">FastAPI でリソース管理エンドポイントを作成</a>

**その 6**: <a href="https://nmomos.com/tips/2021/02/21/fastapi-docker-6/" target="_blank">ユーザーモデルの実装</a>

**その 7**: <a href="https://nmomos.com/tips/2021/02/21/fastapi-docker-7/" target="_blank">JWTトークンの実装</a>

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

テストの実行

```bash
$ docker-compose exec server pytest -vv
```

---

## API Document へのアクセス

**Swagger:**
<a href="http://localhost:8000/docs" target="_blank">
http://localhost:8000/docs
</a>

**Redoc:**
<a href="http://localhost:8000/docs" target="_blank">
http://localhost:8000/redoc
</a>
