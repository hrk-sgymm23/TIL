# Dockerの基本::基本コマンド  

## imageを取得・ビルドする

### `pull` レジストリより取得する
```bash
# レジストリへログイン
$ docker login -u <コンテナレジストリのユーザー名> -p <コンテナレジストリのパスワード> <コンテナレジストリのログインサーバー>
# DockerHubから任意のDockerイメージ(imagename)を取得する場合
# docker pull <コンテナイメージの公開パス:タグ>
$ docker pull imagename
```

### `build`Dockerfileよりビルドする
```bash
# Dockerfileがカレントディレクトリにある場合
$ docker image build .

#　タグを付ける場合（-tオプション）
#　タグの書式：　　名前空間/イメージ名:タグ名
# docker build -t <コンテナイメージ名:タグ> <Dockerfileが存在するディレクトリ>
$ docker build -t test/apache:latest .

#　ファイル名を指定する場合（-fオプション）
$ docker build -f Dockerfile-test .
```

### `ls`image一覧取得
```bash
# 現在のイメージの一覧を確認する
$ docker image ls
```

### image削除
```bash
$ docker rmi <イメージID>
```

## コンテナを生成・起動
```bash
$ docker start <コンテナID>

# 書式：docker container run [オプション] イメージ [コマンド]
$ docker container run test/apache:latest

# コンテナをバックグランドで実行する（-dオプション）
$ docker container run　 -d test/apache:latest

# コンテナに名前を付ける(--nameオプション)
$ docker container run --name apache_test test/apache:latest

# 標準出力とターミナルをアタッチする（-itオプション）
$ docker container run　 -it test/apache:latest
```
- `-it`オプションに関して...interactiveの`-i`とttyの`-t`を合わせたオプションでコンテナ上で実行されるプロセスがシェルの場合、`-it`をつけることによりコンテナを修了せずに使用できる

## コンテナの削除
```bash
$ docker rm <コンテナID>
```

## `ps`コンテナの状態確認
```bash
$ docker ps
# 停止中のものも表示
$ docker ps -a
```

## ログを確認`docker container logs`
```bash
# 書式：　docker container logs [オプション] コンテナ
$ docker container logs apache
```


## コンテナ内でコマンド実行`exec`
```bash
# 書式：　docker container exec [オプション] コンテナ コマンド [引数]
$ docker container exec apache ls /

# -itオプション
# 標準出力とターミナルをアタッチする（interactive,tty）　→　シェルを終了させない
$ docker container exec -it apache /bin/bash
```

## コンテナを停止・削除する
### コンテナを停止
```bash
$ docker stop <コンテナID>
```
### コンテナを削除する
```bash
$ docker rm <コンテナID>
```

### コンテナイメージを削除する
```bash
$ docker rmi <コンテナイメージID>
```
