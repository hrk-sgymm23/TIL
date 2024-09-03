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
 --parameters '{"host":["ass-staging.c3e2e24uwy59.ap-northeast-1.rds.amazonaws.com"],"portNumber":["3306"], "localPortNumber":["80"]}'

Starting session with SessionId: botocore-session-1725371830-eykx37cqw7lyrub3brtmzsi7ce
```




