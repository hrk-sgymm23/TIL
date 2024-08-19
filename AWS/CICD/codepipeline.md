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

# タスク定義ファイル(動的に値が取れるもの)とappspec.ymlをS3へ格納

