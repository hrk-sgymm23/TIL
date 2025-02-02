# Golangの開発環境を作る

https://github.com/hrk-sgymm23/zenn_notify_app

## Lambda周りのセットアップ

下記を確認する。
https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/golang-handler.html#golang-handler-setup

# RIEを使う

- https://github.com/aws/aws-lambda-runtime-interface-emulator
- https://docs.aws.amazon.com/lambda/latest/dg/images-create.html

## 以下chatgptの説明

RIE の使い方
1. 前提条件
Docker がインストールされていること。
Golang で作成された Lambda 関数のコードが準備されていること。
2. Lambda 関数コードの準備
以下は、簡単な Go ランタイム用 Lambda ハンドラーの例です。

```go
// main.go
package main

import (
	"context"
	"fmt"

	"github.com/aws/aws-lambda-go/lambda"
)

type MyEvent struct {
	Name string `json:"name"`
}

func handler(ctx context.Context, event MyEvent) (string, error) {
	return fmt.Sprintf("Hello, %s!", event.Name), nil
}

func main() {
	lambda.Start(handler)
}
```
このコードは、リクエスト JSON の name フィールドに基づいてレスポンスを返すシンプルな Lambda 関数です。

3. Docker イメージの作成
Dockerfile を作成 以下は Go ランタイム用の `Dockerfile` の例です。
`dockerfile`
```dockerfile
FROM golang:1.20 as builder

# Lambda 関数コードをコンテナにコピー
WORKDIR /app
COPY . .

# 実行ファイルをビルド
RUN go mod init example-lambda && \
    go mod tidy && \
    GOOS=linux GOARCH=amd64 go build -o main

# AWS Lambda Runtime Interface Emulator を使用したランタイム
FROM public.ecr.aws/lambda/go:latest

# ビルドした実行ファイルと RIE をコピー
COPY --from=builder /app/main /var/task/

# エントリポイントを設定
CMD ["main"]
```
イメージのビルド 次のコマンドで Docker イメージをビルドします。
```bash
docker build -t lambda-go-rie-example .
```

4. ローカルで実行
ビルドしたイメージを使用して、ローカルで Lambda を実行します。

Docker コンテナを起動 以下のコマンドで Docker コンテナを起動します。
```bash
docker run -p 9000:8080 lambda-go-rie-example
```
このコマンドは、9000 番ポートでリクエストを受け付けるように設定します。

リクエストを送信 以下のように curl コマンドを使ってリクエストを送信できます。
```bash
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
    -d '{"name": "World"}'
```

5. レスポンスの確認
上記のリクエストを送信すると、以下のようなレスポンスが得られるはずです。

```json
"Hello, World!"
```

6. 環境変数の設定
環境変数を設定したい場合、`docker run`コマンドに`-e` オプションを追加します。

```bash
docker run -p 9000:8080 -e MY_ENV_VAR=my-value lambda-go-rie-example
```

参考リンク
AWS Lambda Runtime Interface Emulator GitHubリポジトリ
AWS Lambda Docker Images公式ドキュメント
上記を実行すると、RIE を使用してローカル環境で Lambda 関数の動作を確認できます！

# RIEではなくLocalStackを使う

https://future-architect.github.io/articles/20200927/

## LocalStackのdocker-compposeファイル

https://docs.localstack.cloud/getting-started/installation/#docker-compose

```yml
services:
  localstack:
    container_name: "${LOCALSTACK_DOCKER_NAME:-localstack-main}"
    image: localstack/localstack
    ports:
      - "127.0.0.1:4566:4566"            # LocalStack Gateway
      - "127.0.0.1:4510-4559:4510-4559"  # external services port range
    environment:
      # LocalStack configuration: https://docs.localstack.cloud/references/configuration/
      - DEBUG=${DEBUG:-0}
    volumes:
      - "${LOCALSTACK_VOLUME_DIR:-./volume}:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
```

```bash
$ docker-compose up -d --build
```

localstackがアクティブか確認
```bash
$ curl -s "http://localhost:4566/_localstack/health" | jq .
```

localstack cliダウンロード
```bash
$ brew install awscli-local
```

## 作業順序

- コンテナ外から関数を確認
```bash
$ aws lambda --profile local --endpoint-url http://localhost:4566 list-functions
```

- コンテナ外でaws cliを使ってラムダを作成
```bash
$ aws lambda create-function --function-name zenn-app-local \
    --endpoint-url http://localhost:4566 \
    --runtime provided.al2 --handler bootstrap \
    --architectures arm64 \
    --role arn:aws:iam::111111111111:role/lambda-runtime-role \
    --zip-file fileb://zenn_app.zip \
    --profile local \
    --timeout 30
```

- 関数を改めて確認
```bash
$ aws lambda --profile local --endpoint-url http://localhost:4566 list-functions
```

- 関数を呼び出す
```bash
$ docker-compose exec localstack /bin/bash

$ awslocal lambda invoke \
    --function-name zenn-app-local \
    --cli-binary-format raw-in-base64-out \
    /tmp/response_simple_function.json
```

- 以下エラーになる
  - Localstack内のCLIのバージョンが古い
```bash
Note: AWS CLI version 2, the latest major version of the AWS CLI, is now stable and recommended for general use. For more information, see the AWS CLI version 2 installation instructions at: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html

usage: aws [options] <command> <subcommand> [<subcommand> ...] [parameters]
To see help text, you can run:

  aws help
  aws <command> help
  aws <command> <subcommand> help

Unknown options: --cli-binary-format, /tmp/response_simple_function.json
root@db3e73e9873a:/opt/code/localstack# aws --version
aws-cli/1.29.5 Python/3.10.12 Linux/5.10.104-linuxkit botocore/1.31.5
root@db3e73e9873a:/opt/code/localstack# aws --version
aws-cli/1.29.5 Python/3.10.12 Linux/5.10.104-linuxkit botocore/1.31.5
```

- コンテナ内から実行はできた
```bash
$ aws lambda invoke \
    --function-name zenn-app-local \
    --cli-binary-format raw-in-base64-out \
    --profile local \
    --endpoint-url http://localhost:4566 \
    /tmp/response_simple_function.json

{
    "StatusCode": 200,
    "FunctionError": "Unhandled",
    "ExecutedVersion": "$LATEST"
}
```

- ログを有効化して確認するところから

- awslocalコンテナないから実行
```bash
$ awslocal lambda invoke \--function-name zenn-app-local /tmp/response_simple_function.json
{
    "StatusCode": 200,
    "FunctionError": "Unhandled",
    "ExecutedVersion": "$LATEST"
}

$ cat /tmp/response_simple_function.json
{"errorMessage":"failed to fetch ZENN_API_URL: failed to fetch parameter ZENN_API_URL: UnrecognizedClientException: The security token included in the request is invalid.\n\tstatus code: 400, request id: 29d7fe11-413e-4f60-b4fb-ea85bb8950ea","errorType":"wrapError"}
```

- localstack内にSSMパラメータストアを作る
```bash
$ aws ssm put-parameter --name 'ZENN_API_URL' --type 'String' --value 'https://zenn.dev/api/articles?topicname=aws&order=trend'
```

上記をlocalstack用に書き換える

```bash
aws ssm put-parameter \
  --name 'ZENN_API_URL'
  --type 'String' \
  --value 'https://zenn.dev/api/articles?topicname=aws&order=trend'
  --profile local \
  --endpoint-url http://localhost:4566
```

- goのパラメータ取得部分見直し
- 以下で解決できそう

https://zenn.dev/jy8752/articles/2b81e42d4ef4f7
https://kazuhira-r.hatenablog.com/entry/2023/07/02/222545

## 詳細なログをとる

```bash
aws --endpoint-url=http://localhost:4566 logs describe-log-groups  --query logGroups[0].logGroupName --profile local
```

## 参考
- https://qiita.com/outerlet/items/a1b8b3e6cc1c690c6d21
- 

