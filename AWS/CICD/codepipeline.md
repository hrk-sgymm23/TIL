# Codepipeline作成

# やること
- GithubActionsにて作成したコンテナイメージがECRに格納されることを起点にCodepipelineを起動し、DBマイグレーション、ECSサービスの更新まで行う。

# 参考
- [ECS用のCDパイプラインに対する考察](https://zenn.dev/reireias/articles/8e987af2762eaa#%E8%B6%A3%E6%97%A8)
  - 様々な種類の構成のパイプラインが載っている
  - 「3. Image BuildのみGitHub Actionsでやる」がやりたいイメージ

#　各Code~の仕組みについて理解する

# CodeBuild

## アーティファクトについて理解する

# CodePipelineの流れ

1. GithubActionsよりECRへコンテナイメージがpushされる
2. 前項にてpushされたイメージを検知し、CodeBuildが発火
3. CodeBuildにてECRからpushされたイメージをもとに
  - DBマイグレーション
  - S3からappspecとタスク定義を取得しアーティファクト化(後続の処理へ渡すための処理)
  - CodeDeployにてECSサービスを更新


# CodeBuild作成時の課題

## S3から取得するタスク定義にてタスク定義のリビジョンを動的にしたい
- [【ECS Blue/Greenデプロイ】１タスクで複数コンテナ稼働している場合のCI/CDパイプライン構築](https://qiita.com/tarian/items/5043abe44345d448e7dc)

**タスク定義の変更はインフラレベルで行うため、terraformから更新された際に更新できる**

今回CDにおいて変更を加えたいのは更新されたコンテナイメージのみのため、コンテナイメージの参照のみ行いたい

## タスク定義ファイル(動的に値が取れるもの)とappspec.ymlをS3へ格納

## Deploy周りのリソース作成
- `aws_codedeploy_app`
- `aws_codedeploy_deployment_group`

## ECS x Codedeplyの場合はデプロイ方法はブルーグリーンのみ

ブルーグリーン実装に当たって必要なリソースの搾り出し
- ターゲットグループ(緑環境用)
- リスナー(プロダクション、テスト)
- リスナールール(プロダクション、テスト)

## ELB リスナーに関して

> リスナーは、設定したプロトコルとポートを使用して、クライアントからの接続リクエストをチェックします。リスナーに対して定義したルールにより、ロードバランサーが登録済みターゲットにリクエストをルーティングする方法が決まります。各ルールは優先度、1 つ以上のアクション、および 1 つ以上の条件で構成されています。ルールの条件が満たされると、アクションが実行されます。リスナーごとにデフォルトのルールを定義する必要があり、オプションで追加のルールを定義できます。
引用: https://docs.aws.amazon.com/ja_jp/elasticloadbalancing/latest/application/introduction.html


## codebuildでエラー
```bash
Error: Error creating CodeBuild project: InvalidInputException: Invalid input: buildspec must be a valid YAML file
```

`source`周りを見直す
```hcl
data "local_file" "buildspec_local" {
    filename = "${path.module}/buildspec.yml.tmpl"
}

source {
    buildspec           = data.local_file.buildspec_local.content
    git_clone_depth     = 0
    insecure_ssl        = false
    report_build_status = false
    type                = "CODEPIPELINE"
  }
```

https://dev.to/seifolahghaderi/terraform-aws-codebuild-embed-buildspec-yml-1ci0
上記にてエラー解消

## Buildステージにてマイグレーションの際にエラー

`Mysql2::Error::ConnectionError: Unknown server host 'ass_db' (-2) (Mysql2::Error::ConnectionError)`

https://qiita.com/matsuda-hiroki/items/fe28e681c4354a16b398

上記記事のようにネットワーク設定を確認する
<img width="912" alt="スクリーンショット 2024-08-30 23 34 39" src="https://github.com/user-attachments/assets/bd19e2e8-5243-4f85-ad17-5ca242add4cf">


## CodeBuildのネットワークを設定する際にエラー
```bash
Error: Error creating CodeBuild project: InvalidInputException: Not authorized to perform DescribeSecurityGroups
```

上記CodeBuild用のロールに`ec2:DescribeSecurityGroups`がないためおこるエラー

## CodebuildにてDBエラー
https://qiita.com/matsuda-hiroki/items/fe28e681c4354a16b398

上記記事のマイグレーションコマンドを試す
```bash
- docker run --rm --env RAILS_ENV=$RAILS_ENV --env SECRET_KEY_BASE=$SECRET_KEY_BASE --env DB_HOST=$DB_HOST --env DB_NAME=$DB_NAME --env DB_USERNAME=$DB_USERNAME --env DB_PASSWORD=$DB_PASSWORD $REPOSITORY_URI:latest rails db:migrate
```

現状
```bash
- docker run --rm -e RAILS_MASTER_KEY -e DATABASE_URL $IMAGE rails db:migrate
```

### 必要なenv
- `RAILS_ENV`
- `SECRET_KEY_BASE`
- `DB_HOST`
- `DB_NAME`
- `DB_USERNAME`
- `DB_PASSWORD`

　完成形
```bash
- docker run --rm -e RAILS_MASTER_KEY RAILS_ENV=staging DB_HOST DB_NAME DB_USERNAME DB_PASSWORD $IMAGE rails db:migrate
```

## DBトラブルシュート
https://qiita.com/itoo/items/ffcf9fe2f1b825ed0720

## 同じ現象の人いた
https://github.com/brianmario/mysql2/issues/1211

## RDSへ接続しコマンドを叩ける状況にしたい
MySQL コマンドラインクライアントからの接続 (非暗号化)
https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/USER_ConnectToInstance.html

```bash
mysql -h ass-staging.c3e2e24uwy59.ap-northeast-1.rds.amazonaws.com -P 3306 -u ass_api -p
```

下記を実行したいが踏み台が必要
https://stackoverflow.com/questions/41200297/mysql2error-cant-connect-to-local-mysql-server-through-socket-tmp-mysql-so
```bash
mysql.server start
```

## 踏み台ECSを作る
- https://qiita.com/hirooka622/items/d9ffb3aaf5fbba0a8a8d
- https://zenn.dev/quiver/articles/1458e453118254

# 踏み台から接続

runtimeidを取得
```bash
aws ecs describe-tasks \
  --cluster <クラスター名> \
  --task <タスクID>
```

```bash
aws ecs describe-tasks \
  --cluster ass-bastion-staging \
  --task b5213840e42d4b39bb7dab71f87b1d49
```

d48b9c7e00b94a98aabb59e9a668bf08-607325679

## SessionManagerからRDS接続
```bash
aws ssm start-session \
 --target "ecs:<クラスター名>_<タスクID>_<ランタイムID> \
 --document-name AWS-StartPortForwardingSessionToRemoteHost \
 --parameters '{"host":["<RDSのエンドポイント>"],"portNumber":["5432"], "localPortNumber":["15441"]}'
```

```bash
aws ssm start-session \
 --target "ecs:ass-bastion-staging_b5213840e42d4b39bb7dab71f87b1d49_b5213840e42d4b39bb7dab71f87b1d49-607325679 \
 --document-name AWS-StartPortForwardingSessionToRemoteHost \
 --parameters '{"host":["ass-staging.c3e2e24uwy59.ap-northeast-1.rds.amazonaws.com"],"portNumber":["3306"], "localPortNumber":["80"]}'
```

## 以下エラーでECSが起動できない

```bash
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:06 INFO Checking if agent identity type OnPrem can be assumed
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:06 ERROR Agent failed to assume any identity
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:06 ERROR failed to get identity: failed to find agent identity
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:06 ERROR Error occurred when starting amazon-ssm-agent: failed to get identity: failed to find agent identity
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:05 ERROR failed to find identity, retrying: failed to find agent identity
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:05 ERROR Agent failed to assume any identity
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:05 INFO Checking if agent identity type OnPrem can be assumed
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:05 ERROR failed to find identity, retrying: failed to find agent identity
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:05 ERROR Agent failed to assume any identity
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:05 INFO Checking if agent identity type OnPrem can be assumed
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:05 INFO no_proxy:
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:05 INFO http_proxy:
-
2024年9月01日 23:08 (UTC+9:00)
2024-09-01 14:08:05 INFO https_proxy:

```

## 上記エラーの解決に講じたこと
- セキュリティグループに443のルール追加
- AmazonSSMManagedInstanceCoreが必要？
  - https://docs.aws.amazon.com/ja_jp/aws-managed-policy/latest/reference/AmazonSSMManagedInstanceCore.html

ssm:*とec2:*を追加

nginxのイメージだったら行けた
`public.ecr.aws/nginx/nginx:latest`

## sessionが始まらない
```bash
aws ssm start-session \
 --target ecs:ass-bastion-staging_38d151a1f1d1414384ba767cf0a83bf8_38d151a1f1d1414384ba767cf0a83bf8-607325679 \
 --document-name AWS-StartPortForwardingSessionToRemoteHost \
 --parameters '{"host":["ass-staging.c3e2e24uwy59.ap-northeast-1.rds.amazonaws.com"],"portNumber":["3306"], "localPortNumber":["1234"]}'

Starting session with SessionId: botocore-session-1725371830-7eqsc4tj4xbw2begql7aql6qum
Port 1234 opened for sessionId botocore-session-1725371830-7eqsc4tj4xbw2begql7aql6qum.
Waiting for connections...
```


## ECS exec実行
```bash
$ aws ecs execute-command --cluster ass-bastion-staging \
    --task arn:aws:ecs:ap-northeast-1:730335441282:task/ass-bastion-staging/45a09fad81884d4fa562256f23f8808b \
    --container bastion \
    --interactive \
    --command "/bin/sh"
```

pingをインストールし実行
下記よりECSタスクよりrdsへ名前解決できている事はわかる
```bash
apt-get update
apt-get install -y iputils-ping

# ping ass-staging.c3e2e24uwy59.ap-northeast-1.rds.amazonaws.com
PING ass-staging.c3e2e24uwy59.ap-northeast-1.rds.amazonaws.com (172.10.2.192) 56(84) bytes of data.
```

## タスク牴牾を修正する
https://repost.aws/ja/questions/QUvGrmH_JpQrGtkizz8kn2_Q/how-do-i-create-an-ssm-agent-to-run-as-a-sidecar-in-ecs-fargate-for-fis-test

```json
{
    "name": "amazon-ssm-agent",
    "image": "public.ecr.aws/amazon-ssm-agent/amazon-ssm-agent:latest",
    "cpu": 0,
    "links": [],
    "portMappings": [],
    "essential": false,
    "entryPoint": [],
    "command": [
        "/bin/bash",
        "-c",
        "set -e; yum upgrade -y; yum install jq procps awscli -y; term_handler() { echo \"Deleting SSM activation $ACTIVATION_ID\"; if ! aws ssm delete-activation --activation-id $ACTIVATION_ID --region $ECS_TASK_REGION; then echo \"SSM activation $ACTIVATION_ID failed to be deleted\" 1>&2; fi; MANAGED_INSTANCE_ID=$(jq -e -r .ManagedInstanceID /var/lib/amazon/ssm/registration); echo \"Deregistering SSM Managed Instance $MANAGED_INSTANCE_ID\"; if ! aws ssm deregister-managed-instance --instance-id $MANAGED_INSTANCE_ID --region $ECS_TASK_REGION; then echo \"SSM Managed Instance $MANAGED_INSTANCE_ID failed to be deregistered\" 1>&2; fi; kill -SIGTERM $SSM_AGENT_PID; }; trap term_handler SIGTERM SIGINT; if [[ -z $MANAGED_INSTANCE_ROLE_NAME ]]; then echo \"Environment variable MANAGED_INSTANCE_ROLE_NAME not set, exiting\" 1>&2; exit 1; fi; if ! ps ax | grep amazon-ssm-agent | grep -v grep > /dev/null; then if [[ -n $ECS_CONTAINER_METADATA_URI_V4 ]] ; then echo \"Found ECS Container Metadata, running activation with metadata\"; TASK_METADATA=$(curl \"${ECS_CONTAINER_METADATA_URI_V4}/task\"); ECS_TASK_AVAILABILITY_ZONE=$(echo $TASK_METADATA | jq -e -r '.AvailabilityZone'); ECS_TASK_ARN=$(echo $TASK_METADATA | jq -e -r '.TaskARN'); ECS_TASK_REGION=$(echo $ECS_TASK_AVAILABILITY_ZONE | sed 's/.$//'); ECS_TASK_AVAILABILITY_ZONE_REGEX='^(af|ap|ca|cn|eu|me|sa|us|us-gov)-(central|north|(north(east|west))|south|south(east|west)|east|west)-[0-9]{1}[a-z]{1}$'; if ! [[ $ECS_TASK_AVAILABILITY_ZONE =~ $ECS_TASK_AVAILABILITY_ZONE_REGEX ]]; then echo \"Error extracting Availability Zone from ECS Container Metadata, exiting\" 1>&2; exit 1; fi; ECS_TASK_ARN_REGEX='^arn:(aws|aws-cn|aws-us-gov):ecs:[a-z0-9-]+:[0-9]{12}:task/[a-zA-Z0-9_-]+/[a-zA-Z0-9]+$'; if ! [[ $ECS_TASK_ARN =~ $ECS_TASK_ARN_REGEX ]]; then echo \"Error extracting Task ARN from ECS Container Metadata, exiting\" 1>&2; exit 1; fi; CREATE_ACTIVATION_OUTPUT=$(aws ssm create-activation --iam-role $MANAGED_INSTANCE_ROLE_NAME --tags Key=ECS_TASK_AVAILABILITY_ZONE,Value=$ECS_TASK_AVAILABILITY_ZONE Key=ECS_TASK_ARN,Value=$ECS_TASK_ARN Key=FAULT_INJECTION_SIDECAR,Value=true --region $ECS_TASK_REGION); ACTIVATION_CODE=$(echo $CREATE_ACTIVATION_OUTPUT | jq -e -r .ActivationCode); ACTIVATION_ID=$(echo $CREATE_ACTIVATION_OUTPUT | jq -e -r .ActivationId); if ! amazon-ssm-agent -register -code $ACTIVATION_CODE -id $ACTIVATION_ID -region $ECS_TASK_REGION; then echo \"Failed to register with AWS Systems Manager (SSM), exiting\" 1>&2; exit 1; fi; amazon-ssm-agent & SSM_AGENT_PID=$!; wait $SSM_AGENT_PID; else echo \"ECS Container Metadata not found, exiting\" 1>&2; exit 1; fi; else echo \"SSM agent is already running, exiting\" 1>&2; exit 1; fi"
    ],
    "environment": [
        {
            "name": "MANAGED_INSTANCE_ROLE_NAME",
            "value": "<SSMManagedInstanceRole>"
        }
    ],
"environmentFiles": [],
    "mountPoints": [],
    "volumesFrom": [],
    "secrets": [],
    "dnsServers": [],
    "dnsSearchDomains": [],
    "extraHosts": [],
    "dockerSecurityOptions": [],
    "dockerLabels": {},
    "ulimits": [],
    "systemControls": []
}
```

## RDSへ接続

https://zenn.dev/fuku710/articles/f4ef9ffe81c3ee

上記を参考に

### タスク定義
```json
[
    {
      "name": "bastion",
      "image": "alpine/socat",
      "cpu": 256,
      "memory": 512,
      "essential": true,
      "pseudoTerminal": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-create-group": "true",
          "awslogs-group": "/ecs/bastion",
          "awslogs-region": "ap-northeast-1",
          "awslogs-stream-prefix": "/ecs/bastion"
        }
      },

      "portMappings": [],
      "command": [
        "tcp4-listen:3306,reuseaddr,fork",
        "tcp-connect:ass-staging.c3e2e24uwy59.ap-northeast-1.rds.amazonaws.com"
      ],
      "environment": [
        {
            "name" : "MANAGED_INSTANCE_ROLE_NAME",
            "value" : "ass-bastion-role"
        }
      ]
    }
]
```

### 実際にポートフォワード

#### `aws ecs describe-tasks`でrunidを入手
```bash
aws ecs describe-tasks \
  --cluster ass-bastion-staging \
  --task 10eead7d2432426bbb054c6a334d05ce
```

#### `ssm start-session`実行
```bash
aws ssm start-session \
 --target ecs:ass-bastion-staging_10eead7d2432426bbb054c6a334d05ce_10eead7d2432426bbb054c6a334d05ce-607325679 \
 --document-name AWS-StartPortForwardingSessionToRemoteHost \
 --parameters '{"host":["ass-staging.c3e2e24uwy59.ap-northeast-1.rds.amazonaws.com"],"portNumber":["3306"], "localPortNumber":["1234"]}'
```

下記挙動になることを確認
```bash
Starting session with SessionId: botocore-session-1725787224-kagek5goi6glg6dg6fpopea7na
Port 1234 opened for sessionId botocore-session-1725787224-kagek5goi6glg6dg6fpopea7na.
Waiting for connections...
```

別シェルでmysqlへ接続
```bash
$ mysql -h 127.0.0.1 -P 1234 -u ass_api -p

$ show databases;\
+--------------------+
| Database           |
+--------------------+
| ass-staging        |
| ass_rds_staging    |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
6 rows in set (0.12 sec)

$ use ass-staging;

$ show tables;
+--------------------------------+
| Tables_in_ass-staging          |
+--------------------------------+
| active_storage_attachments     |
| active_storage_blobs           |
| active_storage_variant_records |
| ar_internal_metadata           |
| location_posts                 |
| schema_migrations              |
| users                          |
+--------------------------------+
7 rows in set (0.09 sec)

$ select * from location_posts;
```

ポートフォワードしたシェルで以下挙動になっていることを確認
```bash
Connection accepted for session [botocore-session-1725787224-kagek5goi6glg6dg6fpopea7na]
```

## TablePlusから接続
<img width="502" alt="スクリーンショット 2024-09-09 23 18 41" src="https://github.com/user-attachments/assets/6c4be803-981a-4178-b4d3-78ddb7ee56f6">


