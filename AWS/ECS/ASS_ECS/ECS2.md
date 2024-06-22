# `exec /usr/bin/entrypoint.sh: exec format error`

https://qiita.com/OmeletteCurry19/items/fd057a7448aa3072fd1e

以下のようにして解消
```bash
$ cd backend/
# --platform linux/amd64をつける
$ docker build --platform linux/amd64  -t ass-rails-ecr-staging .
$ docker tag ass-rails-ecr-staging:latest 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/ass-rails-ecr-staging:stg
```

## 一旦リソース削除

RDS,ALB,ECSは削除→戻す際は依存関係に気を付ける

## DBのスナップショットが有効になっていたため調査
```terraform
resource "aws_db_instance" "main" {
~
  skip_final_snapshot             = true
~
```
`skip_final_snapshot`をtrueにすることで削除する際にスナップショットを作成しなくできる。
