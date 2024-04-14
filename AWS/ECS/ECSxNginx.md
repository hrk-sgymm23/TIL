# ECSを使ってNginxで`HelloWorld`

## 参考
- [Amazon ECS クラスターの NGINX ワークロードのサンプル(公式Doc)](https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/monitoring/ContainerInsights-Prometheus-Setup-nginx-ecs.html)
- [Amazon ECSでFargateを使ってNginxコンテナを起動し「Hello Wolrd」を表示してみる](https://zenn.dev/shimiyu/articles/3b6cacf157112f)

# ECR

### ECR作成
#### ECRの認証

- Assume確認
```bash
$ aws sts get-caller-identity --profile ecs_developer

{
    "UserId": "AROA2UC3COxxxxxxxxx-session-1713088067",
    "Account": "730335xxxxxxx",
    "Arn": "arn:aws:sts::7303xxxxx:assumed-role/SwitchRoleAdministrator/botocore-session-1713088067"
}
```
- 認証
```bash
$ aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com

Login Succeeded
```

### イメージのpush

#### イメージビルド
```bash
$ docker build -t 0414-nginx-test .
```

#### イメージにタグつけ
```bash
$ docker tag 0414-nginx-test:latest 73033XXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/0414-nginx-test:latest
```

#### push
```bash
$ docker push 7303xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/0414-nginx-test:latest

The push refers to repository [7303xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/0414-nginx-test]
57b99ff134c9: Pushed
4280bf75d59a: Pushed
a15f6df32c16: Pushed
260571b9b9ec: Pushed
7b795f132dec: Pushed
bae3e6fa3b43: Pushed
21ec097e7be7: Pushed
latest: digest: sha256:426c49114be3275ccec222be875384d6b01a618ebc3f0f57a9fe1cfc10eb571f size: 1777
```

# ALB

## VPC作成
- `ecs-nginx-vpc`

## ALB作成
- `alb-1`
  - `ap-northeast-1a`
  - `10.0.0.64/26`
- `alb-2`
  - `ap-northeast-1c`
  - `10.0.0.0/26`

## IGW
- `ecs-nginx-igw`
　　- `ecs-nginx-vpc`にアタッチ

## ルートテーブル
- 送信先: `0.0.0.0/0`
- ターゲット: `ecs-nginx-igw`

## サブネット作成

