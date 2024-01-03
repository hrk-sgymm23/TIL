# Dockerの基礎::Dockerfileの書き方について

## dockerfileについて
- dockerfileはドッカーイメージを作成するためのイメージファイル
- dockerfileには基本となるOS、インストールするソフトウェア、コピーするファイル・ディレクトリ、開くポート、実行するコマンドなど新しいイメージを作成するための必要な指示が含まれる
- dockerfileの書き方としては「FROM」,「RUN」,「CMD」などのインストラクションに引数を記述し、作成する

<img width="708" alt="スクリーンショット 2024-01-03 17 17 38" src="https://github.com/hrk-sgymm23/TIL/assets/78539910/e5cb4a70-0c82-4faf-ba66-105ccf49c479">

## 各インストラクションについて
### `FROM`
- 新たに作成するDockerイメージのベースとなるイメージを指定する

```Dockerfile
# 書式：　FROM [イメージ] [タグ]
$ FROM　ubuntu:22.10
```

### `RUN`
- `RUN`はDockerイメージのビルドの際にシェルコマンドを実行する
```Dockerfile
# 書式：　RUN [コマンド] 
$ RUN apt update \
    && apt install -y apache2
```
- `RUN`は実行ごとに新しいレイヤーを作成しての上でコマンドを実行するため、多くの`RUN`を持つファイルは多くのレイヤーからなるイメージを作成し、イメージのサイズが大きくなる
- しかしレイヤ数が多くなるとPCの容量が多くなり圧迫されたり、イメージのビルドに時間がかかるため、レイヤ数は最小にすることが望ましい
- このため複数コマンドを実行する際は`&&` でつなぎ`\`で改行を入れることが望ましい

### `CMD`
- Dockerコンテナで実行された時にデフォルトで実行するコマンドを定義する

```dockerfile
# 書式：　CMD ["実行ファイル", "パラメータ1","パラメータ2"] 
$ CMD ["apachectl","-D","FOREGROUND"]
```
> [!NOTE]
> `RUN`と`CMD`の違いとは...引数にあるコマンドを受け取るという意味では似ているが`RUN`はレイヤを作るが`CMD`はレイヤを作らない。レイヤは再生可能であり、Dockerは一度ビルドされたキャッシュして再利用できるため、ソフトウェアやファイルのコピーはイメージ構築に必要な手順である`RUN`で指示することでベースイメージにキャッシュさせ覚えさせることで何度もダウンロードさせないようにする

### `COPY`
- ホストやローカルのファイルやディレクトリをdockerイメージにコピーする
- 具体的な使い方として、ソースコードやconfigファイルはローカルで作成してコピーさせる
```dockerfile
# 書式：　COPY [コピー元][コピー先] 
①ファイルをファイルに
$ COPY　index.html /mydir/index.html 
②ファイルをディレクトリ以下に
$ COPY　index.html　/mydir/ 
③ディレクトリをディレクトリに            
$ COPY src/ /mydir/
```

### `ENV`
- dockerfile内で環境変数を設定することができる
- 設定された環境変数はdockerfileにて利用できる
- また作成されたdockerイメージから作成される全てのコンテナ内で利用可能
```dockerfile
# 書式：　ENV [キー]　＝　[値] 
$ ENV MYSQL_USER=admin
$ ENV MYSQL_PASSWORD=password
```

### `WORKDIR`
- コマンドを実行する作業ディレクトリを指定する
```dockerfile
# 書式：　WORKDIR [ディレクトリのパス] 
$ WORKDIR /app
```
- `WORKDIR`を利用することでdockerfileが読みやすくなりパスを何度も書く手間が省ける
