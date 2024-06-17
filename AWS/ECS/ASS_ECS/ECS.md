x# ECS作成

## `aws_caller_identity`について
[*.tf 内で AWS アカウント ID を自動参照(取得)する aws_caller_identity Data Source](https://qiita.com/gongo/items/a2b83d7402b97ef43574)

> ハードコーディングで構わないと思いつつも、どうにかいい感じに Terraform が AWS アカウント ID を取得してくれないかなーという願いを叶えるために、 Terraform version 0.7.1 から aws_caller_identity が実装されました。

# `CloudWatch Container Insights`について
- [Container Insights を使用して Amazon ECS コンテナをモニタリングする](https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/cloudwatch-container-insights.html)
- [Amazon ECS Container Insights メトリクス](https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/monitoring/Container-Insights-metrics-ECS.html)
- [ECS で Container Insights を使ってみた](https://qiita.com/sugimount-a/items/7c62582972a80deccd7d)

> Container Insights では、コンテナ化されたバージョンの CloudWatch エージェントを使用してクラスターで実行中のすべてのコンテナを検出し、パフォーマンススタックのすべてのレイヤーでパフォーマンスデータを収集します。運用データは、パフォーマンスログイベントとして収集されます。これらは、高濃度データを大規模に取り込み、保存できる、構造化された JSON スキーマを使用するエントリです。CloudWatch はこのデータから、クラスター、サービスおよびサービスレベルで、高レベルの集約されたメトリクスを CloudWatch メトリクスとして作成します。このメトリクスには、CPU、メモリ、ディスク、ネットワークなどのリソース使用率が含まれます。メトリクスは、CloudWatch 自動ダッシュボードで使用できます。

# ECSのネットワークモードについて
[https://zenn.dev/fdnsy/articles/43b7f4d745ed1f](https://zenn.dev/fdnsy/articles/43b7f4d745ed1f)

> ECSの起動タイプは2つの選択肢があります。
サーバレス型の「Fargate」
ホスト型の「EC2」

Fargateのネットワークモードはawsvpcのみなので、今回はあまり関係ありません。
EC2を選択した場合に複数の選択肢があるため、今回はこちらのネットワークモードが中心です。
<img width="891" alt="スクリーンショット 2024-05-17 14 55 58" src="https://github.com/hrk-sgymm23/TIL/assets/78539910/a02b68f1-fcf7-43a3-b0f3-f0f4aa472ec3">

# `PassRole`について
[IAMのPassRoleとセキュリティの話](https://qiita.com/koheiawa/items/044a1ccf08482287da16)
> IAMのPassRoleは、IAMポリシーの記述の中で iam:PassRole と表現するアクセス許可です。これは ポリシーがアタッチされているプリンシパル(IAMユーザとIAMロール) が、 AWSのサービス(EC2やLambdaなど) にロールを渡すことを意味しています。これにより、例えばEC2がS3のファイルを読み取れたり、LambdaがDynamoDBにデータを格納することができるようになります。

# 次作業
- ECSモジュールよりタスク実行ロールとしてIAMモジュールを参照
- ECSモジュール作成

# タスク定義を書く
[ECSタスク定義をコンソールから作って後悔した後、コード管理するため最速でJSON登録可能にする超愚直な方法](https://dev.classmethod.jp/articles/ecs-task-definition-to-json/)

> ECSタスク定義で利用できるJSONを作る方法
> 元ネタのJSONを取得する
> 最初に編集するための元ネタとなるJSONを取得します。今回のJSONはマネジメントコンソールにのみ表示されているので、ものすごい愚直な方法でとってきますYO
> マネジメントコンソールのECSタスク定義メニューから該当のタスク定義を開きます。ここで[Create new revision]をクリック。

## `apply`の際のエラー解決
```bash
│ Error: Unsupported attribute
│
│   on ecs.tf line 7, in module "ecs_stg":
│    7:   target_group_arn          = module.alb_stg.target_group_arn
│     ├────────────────
│     │ module.alb_stg is a object
│
│ This object does not have an attribute named "target_group_arn".
```

↑ALBのモジュールのoutputが空だった。

`alb/output.tf`追記
```terraform
output "target_group_arn" {
  value = aws_lb_target_group.main.arn
}

output "dns_name" {
  value = aws_lb.main.dns_name
}

output "zone_id" {
  value = aws_lb.main.zone_id
}
```

```bash
╷
│ Error: Reference to undeclared module
│
│   on ecs.tf line 13, in module "ecs_stg":
│   13:   rails_ecr_arn             = module.rails_ecr_arn
│
│ No module call named "rails_ecr_arn" is declared in the root module.
╵
╷
│ Error: Invalid value for input variable
│
│   on ecs.tf line 14, in module "ecs_stg":
│   14:   nginx_ecr_arn             = module.nginx_ecr_stg
│
│ The given value is not suitable for module.ecs_stg.var.nginx_ecr_arn declared at ../../../modules/ecs/variable.tf:61,1-25: string required.
```
モジュールの指定の仕方が違う

```terraform
  - rails_ecr_arn             = module.rails_ecr_arn
  - nginx_ecr_arn             = module.nginx_ecr_stg
  + rails_ecr_arn             = module.rails_ecr_arn
  + nginx_ecr_arn             = module.nginx_ecr_stg
```

```bash
│ Error: Reference to undeclared module
│
│   on ecs.tf line 15, in module "ecs_stg":
│   15:   ssm_db_password_path      = module.ssm_db_password_path
│
│ No module call named "ssm_db_password_path" is declared in the root module.
╵
```

上記に関しては例`module.ass_rds_stg.ssm_db_password_path`で解決

# Terraformにおけるポリシー作成について
```terraform
data "aws_iam_policy" "ecs_task_execution_role_policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

data "aws_iam_policy_document" "ecs_task_execution" {
  source_policy_documents = [data.aws_iam_policy.ecs_task_execution_role_policy.policy]
  statement {
~
```

## `[]`で囲む理由
`source_policy_documents`は配列型の属性であるため、単一のデータであっても`[]`で囲む必要がある。

## `data.aws_iam_policy.ecs_task_execution_role_policy.policy`の`.policy`の意味
- .policy属性は`aws_iam_policy`から取得したJSON文字列を指す。
- `source_policy_documents`はポリシーを指定する必要がある。.policyをつけることでJSON文字列をpolicyドキュメントとして作成し含めることができる、

# Rails　masterkeyを設定する
- Railsのマスタキーいかに作成される
  - `config/credentials.yml.enc`
- また以下のコマンドで生成を実行可能
```bash
$ rails credentials:edit
```

- 上記キーをパラメータストアに含める
```terraform
data "aws_ssm_parameter" "rails_master_key" {
  name = "/${var.common_name}-${var.environment}/rails-master-key"
}
```

# リバースプロキシ用のコンテナを立てる(ECS作成)
- [【ポートフォリオをECSで！】Rails×NginxアプリをFargateにデプロイするまでを丁寧に説明してみた(VPC作成〜CircleCIによる自動デプロイまで) 前編](https://qiita.com/maru401/items/8e7d32a8baded045adb2#2-nginx)
- [Fargateにおけるpuma+Nginxのソケット通信のやり方](https://bluepixel.hatenablog.com/entry/2020/04/22/230721)


## Dockerfile作成
```dockerfile
FROM nginx:latest
# for health check
RUN apt-get update && apt-get install -y curl
ADD custom.conf /etc/nginx/conf.d
CMD /usr/sbin/nginx -g 'daemon off;'
EXPOSE 80
```

## custom.conf作成
```custom.conf
server {
    listen 80 default_server;

    root /usr/src/app/public;

    location / {
        try_files $uri $uri/index.html $uri.html @puma;
    }

    location @puma {
        proxy_set_header    Host $http_host;
        proxy_set_header    X-Real-IP $remote_addr;
        proxy_set_header    X-Forwarded-Host $host;
        proxy_set_header    X-Forwarded-Server $host;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://my_app;
    }
}

upstream my_app {
    server unix:///usr/src/app/tmp/sockets/puma.sock;
}
```

## Pumaの作成
[[Rails] Nginx × Pumaを連携させる方法](https://zenn.dev/machamp/articles/rails-puma-nginx)

```custom.conf
server {
    listen 80 default_server;

    root /usr/src/app/public;

    location / {
        try_files $uri $uri/index.html $uri.html @puma;
    }

    location @puma {
        proxy_set_header    Host $http_host;
        proxy_set_header    X-Real-IP $remote_addr;
        proxy_set_header    X-Forwarded-Host $host;
        proxy_set_header    X-Forwarded-Server $host;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://my_app;
    }
}

upstream my_app {
    server unix:///usr/src/app/tmp/sockets/puma.sock;
}
```

# ECS作成

# ECRへpush

## Nginx
```bash
$ cd nginx
$ export AWS_PROFILE=root_ecs_developer
$ export AWS_DEFAULT_REGION=ap-northeast-1
$ aws configure list

      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile       root_ecs_developer              env    ['AWS_PROFILE', 'AWS_DEFAULT_PROFILE']
access_key     ****************7BPK shared-credentials-file
secret_key     ****************g9Ps shared-credentials-file
    region           ap-northeast-1              env    ['AWS_REGION', 'AWS_DEFAULT_REGION']

$ aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com

Login Succeeded

$ docker build -t ass-nginx-ecr-staging .
# タグつけ(stg)
$ docker tag ass-nginx-ecr-staging:latest 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/ass-nginx-ecr-staging:stg
$ docker push 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/ass-nginx-ecr-staging:stg
```

## Rails
```bash
$ cd backend
$ docker build -t ass-rails-ecr-staging .
$ docker tag ass-rails-ecr-staging:latest 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/ass-rails-ecr-staging:stg
$ docker push 730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/ass-rails-ecr-staging:stg
```

#　ECS作成

##　apply時にエラー1
```bash
 Error: creating ECS Task Definition (ass-task-def-staging): ClientException: Role is not valid
│
│   with module.ecs_stg.aws_ecs_task_definition.main,
│   on ../../../modules/ecs/main.tf line 25, in resource "aws_ecs_task_definition" "main":
│   25: resource "aws_ecs_task_definition" "main" {
│
```

### Iamのモジュールのアウトプットが違った
```terraform
output "iam_role_arn" {
- value = aws_iam_policy.main.arn
+ value = aws_iam_role.main.arn
}
```

##　apply時にエラー2
```bash
│ Error: creating ECS Service (ass-staging): InvalidParameterException: Health check grace period is only valid for services configured to use load balancers
│
│   with module.ecs_stg.aws_ecs_service.main,
│   on ../../../modules/ecs/main.tf line 88, in resource "aws_ecs_service" "main":
│   88: resource "aws_ecs_service" "main" {
│
╵
```

### サービスのロードバランサーの設定がなかったため
```terraform
resource "aws_ecs_service" "main" {
~
  load_balancer {
    target_group_arn = var.target_group_arn
    container_name = "nginx"
    container_port = 80
  }
~
```

## ECSが落ちる→ログが取れない
```
The specified log stream does not exist.
```

```
InternalError: failed to create container model: failed to normalize image reference "arn:aws:ecr:ap-northeast-1:730335441282:repository/ass-rails-ecr-staging:stg". Launch a new task to retry.
```

### タスク定義のイメージのパスが違う

#### arnではなくURI

- 誤り
```json
{
~
  "image": "arn:aws:ecr:ap-northeast-1:730335441282:repository/ass-rails-ecr-staging:stg",
~
}
```

- 正
```json
{
~
  "image": "730335441282.dkr.ecr.ap-northeast-1.amazonaws.com/ass-rails-ecr-staging:stg",
~
}
```
上記へ修正してもタスクは輝度しない

# ECR周りを確認する

<img width="706" alt="スクリーンショット 2024-06-17 23 31 58" src="https://github.com/hrk-sgymm23/TIL/assets/78539910/346754cc-50d9-4519-b5be-c1a223e5164c">

## VPCエンドポイント作成orECRリソースポリシー編集

### VPCエンドポイントを作成する
- [ECRにpushしたコンテナをECSFargateで使うVPCエンドポイントTerraform例](https://qiita.com/fuubit/items/ab3f682bf59ffeb88d45)
- 







