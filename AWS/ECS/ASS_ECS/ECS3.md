# リソースを復活させる

## NATgatewayが必ず差分として出てきてしまう。。

### `ignore_changes`を使うとリソースの変更を無視できる？
https://dev.classmethod.jp/articles/note-about-terraform-ignore-changes/

#### ignore_changesのユースケース
> : 実体を正としたい
例えば、以下のように「この値は常にTerraformコードの設定を保つ必要がなく、実体を正としたい」といった場合が最も適したユースケースと言えそうです。
> AutoScalingGroupのEC2の起動数
運用開始後は自由にスケールしてほしい
リソースへのタグ付け
他要因によって付けられたタグをTerraformで削除してほしくない

### リソースの属性の変更を無視するものでリソース自体を無視することはできない、、
結局コメントアウトに。。。

## ALBに関して(料金)
- https://aws.amazon.com/jp/elasticloadbalancing/pricing/
- https://qiita.com/T_unity/items/f1be3704072f439dc807
- https://qiita.com/himorishuhei/items/1066c5c579be6de0441c

### 料金の体系
- 時間
- LCU(Load Balancer Capacity Units)

### 料金計算
- 時間
  - USD 0.0243/1h *  24 * 30 = 17.496$ *2 = 35$
- LCU
　　- トラフィックがほぼないため考慮しない

# ECSデプロイ

## SSMのエラー
```bash
ResourceInitializationError: unable to pull secrets or registry auth: unable to retrieve secrets from ssm: The task cannot pull secrets from AWS Systems Manager. There is a connection issue between the task and AWS Systems Manager Parameter Store. Check your task network configuration. RequestCanceled: request context canceled caused by: context deadline exceeded
```
[Amazon ECS 環境変数を使用して Systems Manager パラメータを取得する](https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/secrets-envvar-ssm-paramstore.html)


## DBConnectionエラー
```bash
ActiveRecord::DatabaseConnectionError: There is an issue connecting with your hostname: ass_db. (ActiveRecord::DatabaseConnectionError)
```

### 考えられる原因
1. `database.yml`の設定
2. ECS実行ロールに不足

https://zenn.dev/fdnsy/articles/d42db2c989a637#%E3%81%BE%E3%81%9A%E3%81%AF%E3%82%BF%E3%82%B9%E3%82%AF%E3%82%92%E7%90%86%E8%A7%A3%E3%81%99%E3%82%8B

```bash
data "aws_iam_policy_document" "ecs_task_execution" {
  source_policy_documents = [data.aws_iam_policy.ecs_task_execution_role_policy.policy]
  statement {
    effect = "Allow"
    actions = [
      "ecr:*",
      "ssm:GetParameters",
      "kms:Decrypt",
      "secretsmanager:GetSecretValue",
      "ssmmessages:CreateControlChannel",
      "ssmmessages:CreateDataChannel",
      "ssmmessages:OpenControlChannel",
      "ssmmessages:OpenDataChannel",
      "logs:*",
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["iam:PassRole"]
    # resources = ["arn:aws:iam::730335441282:role/ecsTaskExecutionRole"]
    resources = ["arn:aws:iam::730335441282:role/ass-ecs-task-execution"]
  }
  statement {
    effect  = "Allow"
    actions = ["ecs:ExecuteCommand"]
    # resources = ["arn:aws:iam::730335441282:role/ecsTaskExecutionRole"]
    resources = ["arn:aws:iam::730335441282:role/ass-ecs-task-execution"]
  }
}
```
### RDSのエンドポイントを設定する
https://qiita.com/hatsu/items/22e11e94a0a981d78efa#databaseyml%E3%81%AE%E7%B7%A8%E9%9B%86
```yaml
production:
  <<: *default
  database: fargate_test
  # 環境変数を読み込むように設定
  password: <%= ENV['DB_PASSWORD'] %>
  username: <%= ENV['DB_USERNAME'] %>
  host: <%= ENV['DB_HOST'] %>
```

https://takelg.com/terraform-aws-rds/

### 最終的な設定
`database.yaml`
```yaml
staging:
  <<: *default
  database: <%= ENV["DB_NAME"] %>
  host: api_staging
  username: api
  password: <%= ENV["API_DATABASE_PASSWORD"] %>
  host: <%= ENV["DB_ENDPOINT"] %>
  username: <%= ENV["DB_USERNAME"] %>
  password: <%= ENV["DB_PASSWORD"] %>
```

## Dockerのエントリーポイントについて理解
https://qiita.com/ist-a-s/items/bc1628230e7ac58e09d1


## ECS Execを使ってコンテナ内を確認する

```bash
aws ecs describe-tasks \
    --cluster ass-ecs-cluster-staging \
    --tasks a84b852fa12b479589b4f7ea7555d326


                        {
                            "name": "ExecuteCommandAgent",
                            "lastStatus": "STOPPED"
                        }
                    ],
                    "cpu": "0"
                }
            ],
            "cpu": "256",
            "createdAt": "2024-07-15T11:09:23.552000+09:00",
            "desiredStatus": "STOPPED",
            "enableExecuteCommand": true,
            "executionStoppedAt": "2024-07-15T11:10:31.502000+09:00",
            "group": "service:ass-staging",
            "healthStatus": "UNKNOWN",
            "lastStatus": "STOPPED",
            "launchType": "FARGATE",
            "memory": "512",
            "overrides": {
                "containerOverrides": [
                    {
                        "name": "nginx"
                    },
                    {
                        "name": "rails"
                    }
                ],
                "inferenceAcceleratorOverrides": []
            },
            "platformVersion": "1.4.0",
            "platformFamily": "Linux",
            "pullStartedAt": "2024-07-15T11:09:44.661000+09:00",
            "pullStoppedAt": "2024-07-15T11:10:10.220000+09:00",
            "startedBy": "ecs-svc/7195836571016647723",
            "stopCode": "TaskFailedToStart",
            "stoppedAt": "2024-07-15T11:11:18.301000+09:00",
            "stoppedReason": "Task failed to start",
            "stoppingAt": "2024-07-15T11:10:41.565000+09:00",
            "tags": [],
            "taskArn": "arn:aws:ecs:ap-northeast-1:730335441282:task/ass-ecs-cluster-staging/a84b852fa12b479589b4f7ea7555d326",
            "taskDefinitionArn": "arn:aws:ecs:ap-northeast-1:730335441282:task-definition/ass-task-def-staging:24",
            "version": 5,
            "ephemeralStorage": {
                "sizeInGiB": 20
            }
        }
    ],
    "failures": []
}
```

```bash

```

## Dockerファイルを作り直す
階層を意識した
```bash
$ docker build -f ./docker/staging/Dockerfile --platform linux/amd64  -t ass-rails-ecr-staging .
```


## 起動しない理由

### タスク定義のヘルスチェックのパスが違った
```json
      "healthCheck": {
        "retries": 10,
        "command": [
          "CMD-SHELL",
          # ここ！
          "curl localhost:3000/api/v1/health_check",
          "\"|| exit 1\""
        ],
```

### 下記nginxエラー
```bash
2024年7月15日 20:45 (UTC+9:00)
2024/07/15 11:45:08 [emerg] 1#1: could not build server_names_hash, you should increase server_names_hash_bucket_size: 64
-
-
2024年7月15日 20:45 (UTC+9:00)
nginx: [emerg] could not build server_names_hash, you should increase server_names_hash_bucket_size: 64
-
~
~
~
```

https://qiita.com/hatsu/items/22e11e94a0a981d78efa#nginxconf%E3%81%AE%E4%BD%9C%E6%88%90

上記を参考に`custom.conf`を編集

## PumaとRailsサーバーの同時起動について調べる
上記を解決することでコンテナにわざわざ入らなくても起動できるはず

```ruby
app_root = File.expand_path('..', __dir__)
bind "unix://#{app_root}/tmp/sockets/puma.sock"
```

上記のunix://#{app_root}/tmp/sockets/puma.sockの実際の値がどうなるか確認

`upstream`の改修
```
    upstream app {
        server unix:///api/tmp/sockets/puma.sock;
    }
```

`puma`再起動
```bash
$ rm /api/tmp/pids/server.pid (rm /app/tmp/pids/server.pid)
$ bundle exec puma -C config/puma.rb
```

https://qiita.com/NaokiIshimura/items/7cb2390243939a34754f

上記がnginxとrailsの構成パターンごとの紹介をしてくれている

https://bluepixel.hatenablog.com/entry/2020/04/22/230721

上記参考にタスク定義見直し(ボリュームの部分)

https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/bind-mount-examples.html

公式ドキュメント

## `aws_ecs_task_definition`ブロックから`volume`を指定
https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_task_definition

```terraform
  volume {
    name = "tmp"
  }
```
