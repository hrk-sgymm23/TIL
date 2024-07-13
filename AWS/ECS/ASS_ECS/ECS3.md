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
