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


