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

## セキュリティグループ
### ALB用のセキュリティグループ
- `ecs-nginx-sg2`
  - プロトコル: `HTPP`
  - インバウンドルール: `0.0.0.0/0`
 
## [ターゲットグループ](https://ap-northeast-1.console.aws.amazon.com/ec2/home?region=ap-northeast-1#TargetGroup:targetGroupArn=arn:aws:elasticloadbalancing:ap-northeast-1:730335441282:targetgroup/ecs-nginx-tg/faa7c46d2e3fe06c)


### 基本的な設定
- ターゲットタイプ
  - ECSの場合`IPアドレス`を選ぶ
  - 名前:`ecs-nginx-tg`
  - プロトコル:ポート
    - `HTPP`:`80`
  - アドレスタイプ:`IPv4`
  - プロトコルバージョン:`HTPP1`

### IPアドレス
- 指定しなくてよし
以下参考
> タスクが起動するとタスク内で起動するコンテナ(今回はnginxコンテナ)に動的にIPアドレスが割り当てられるのですが、ECSサービスが自動でターゲットグループにIPアドレスを登録してくれます。そのため、ターゲットグループに手動でIPアドレスを指定する必要はないのです。

> ただし、ECSサービスを作成するときに、ターゲットタイプがIPアドレスのターゲットグループを指定する必要はあります。後ほどECSサービスを作成するときに、ここで作成したecs-target-groupを指定します。


## [ロードバランサー](https://ap-northeast-1.console.aws.amazon.com/ec2/home?region=ap-northeast-1#LoadBalancer:loadBalancerArn=arn:aws:elasticloadbalancing:ap-northeast-1:730335441282:loadbalancer/app/ecs-nginx-alb/0bf413525f886a3e;tab=listeners)

### ALB作成
- `ecs-nginx-alb`作成
  - スキーム:インターネット向け
  - IPアドレスタイプ:IPv4
  - vpc:`ecs-nginx-vpc`
    - サブネット:`subnet-041c491b3324044a5`,`subnet-020a0a767de21c63f`
    - セキュリティグループ:`ecs-nginx-sg2`
    - ターゲットグループ:`ecs-nginx-tg`
    - リスナーとルーティング:`HTTP`,`80`
   

## ECS

### [タスク定義](https://ap-northeast-1.console.aws.amazon.com/ecs/v2/task-definitions/nginx-ecs-task-def/1/containers?region=ap-northeast-1)
- 名前:`nginx-ecs-task-def`

#### インフラストラクチャの要件
- 機動タイプ:`Fargate`
- オペレーティングシステム/アーキテクチャ: `Linux/X86_64`→`ARM/64`に変更することでMacのアーキテクチャで対応できる
- タスクサイズ
  - CPU:`.5vCPU`
  - メモリ:`1GB`
- タスクロール:なし
- 実行ロール:新規作成

#### コンテナ
- コンテナの詳細
  - `nginx-ecs`
  - ECRのURI
- ポートマッピング
  - ポート:`80`
  - プロトコル:`TCP`
  - ポート名:`ecs-nginx-tcp`
  - アプリケーションプロトコル:`HTTP`
- リソース割当制限
  - CPU:`0.5`
  - GPU:`1`
  - メモリのハード制限:`1GB`
  - メモリのソフト制限:`1GB`

### ECSサービス

#### ECSクラスター
- 名前:`ecsnginxcluster`
- インフラストラクチャ:`Fargate`

#### ECSサービス
- 環境
  - `ecsnginxcluster`
  - コンピューティングオプション：`起動タイプ`,`Fargate`
- デプロイ設定
  - アプリケーションタイプ:`サービス`
  - ファミリー:`nginx-ecs-task-def`
  - サービス名:`ecs-nginx-service`
- ネットワーキング
  - vpc:`ecs-nginx-vpc`
  - [サブネット](https://ap-northeast-1.console.aws.amazon.com/vpcconsole/home?region=ap-northeast-1#SubnetDetails:subnetId=subnet-0efc186a708ee71c3):`ecs-subnet`
  - セキュリティグループ:`ecs-nginx-sg2`
- ロードバランシング
  - `Application Load Balancer`
  - コンテナ:`nginx-ecs 80:80`
  - ロードバランサー：`ecs-nginx-alb`
  - リスナー:`80:HTTP`
  - ターゲットグループ:`ecs-nginx-tg`
 
## 成果物
http://ecs-nginx-alb-1719510677.ap-northeast-1.elb.amazonaws.com/












