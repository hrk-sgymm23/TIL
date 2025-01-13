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
